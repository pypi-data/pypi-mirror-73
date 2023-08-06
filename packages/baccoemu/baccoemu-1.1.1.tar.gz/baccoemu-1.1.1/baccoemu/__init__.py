import numpy as np
import copy
import pickle
import progressbar
import hashlib
from ._version import __version__

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _transform_space(x, space_rotation=False, rotation=None, bounds=None):
    """Normalize coordinates to [0,1] intervals and if necessary apply a rotation

    :param x: coordinates in parameter space
    :type x: ndarray
    :param space_rotation: whether to apply the rotation matrix defined through
                           the rotation keyword, defaults to False
    :type space_rotation: bool, optional
    :param rotation: rotation matrix, defaults to None
    :type rotation: ndarray, optional
    :param bounds: ranges within which the emulator hypervolume is defined,
                   defaults to None
    :type bounds: ndarray, optional
    :return: normalized and (if required) rotated coordinates
    :rtype: ndarray
    """
    if space_rotation:
        #Get x into the eigenbasis
        R = rotation['rotation_matrix'].T
        xR = copy.deepcopy(np.array([np.dot(R, xi)
                                     for xi in x]))
        xR = xR - rotation['rot_points_means']
        xR = xR/rotation['rot_points_stddevs']
        return xR
    else:
        return (x - bounds[:, 0])/(bounds[:, 1] - bounds[:, 0])


def _bacco_evaluate_emulator(emulator, coordinates, gp_name='gpy', values=None, sample=False):
    """
    Function evaluating the emulator at some given points.

    :param emulator: the trained gaussian process
    :type emulator: obj
    :param coordinates: points where to predict the function
    :type coordinates: array-like
    :param gp_name: type of gaussian process code to use; options are 'gpy',
                    'george' and 'sklearn', defaults to 'gpy'
    :type gp_name: str
    :param values: only for 'george', the original evaluations of the gp at the
                   coordinates used for training, defaults to None.
    :type values: array-like
    :param sample: only for 'george', whether to take only one sample of the
                   prediction or the full prediction with its variance; if
                   False, returns the full prediction, defaults to False
    :type sample: bool

    :returns: emulated values and variance of the emulation.
    :rtype: float or array_like
    """

    if gp_name == 'gpy':
        deepGP = False
        if deepGP is True:
            res = emulator.predict(coordinates)
            evalues, cov = (res[0].T)[0], (res[1].T)[0]
        else:
            res = emulator.predict(coordinates)
            evalues, cov = (res[0].T)[0], (res[1].T)[0]
    elif gp_name == 'sklearn':
        evalues, cov = emulator.predict(coordinates, return_cov=True)
    elif gp_name == 'george':
        if sample:
            evalues = emulator.predict(values, coordinates)
            cov = 0
        else:
            #import ipdb; ipdb.set_trace()
            # (coordinates,mean_only=False)
            evalues, cov = emulator.predict(
                values, coordinates, return_var=True)
    else:
        raise ValueError('emulator type {} not valid'.format(gp_name))

    return evalues, np.abs(cov)


def _compute_camb_spectrum(params, kmax=50, k_per_logint=0):
    """
    Calls camb with the current cosmological parameters and returns a
    dictionary with the following keys:
    kk, pk

    Through the species keyword the following power spectra can be obtained:
    matter, cdm, baryons, neutrinos, cold matter (cdm+baryons), photons,
    divergence of the cdm velocity field, divergence of the baryon velocity
    field, divergence of the cdm-baryon relative velocity field
    """
    import camb
    from camb import model, initialpower

    if 'tau' not in params.keys():
        params['tau'] = 0.0952
    if 'num_massive_neutrinos' not in params.keys():
        params['num_massive_neutrinos'] = 3 if params['neutrino_mass'] != 0.0 else 0
    if 'Neffective' not in params.keys():
        params['Neffective'] = 3.046
    if 'omega_k' not in params.keys():
        params['omega_k'] = 0
    if 'omega_cdm' not in params.keys():
        params['omega_cdm'] = (params['omega_matter'] - params['omega_baryon'] -
                               params['neutrino_mass'] / (93.14 * params['hubble']**2))

    assert params['omega_k'] == 0, 'Non flat geometries are not supported'

    expfactor = params['expfactor']

    # Set up a new set of parameters for CAMB
    pars = camb.CAMBparams()

    # This function sets up CosmoMC-like settings, with one massive neutrino and helium set using BBN consistency
    # Set neutrino-related parameters
    # camb.nonlinear.Halofit('takahashi')
    pars.set_cosmology(
        H0=100 * params['hubble'],
        ombh2=(params['omega_baryon'] * params['hubble']**2),
        omch2=(params['omega_cdm'] * params['hubble']**2),
        omk=params['omega_k'],
        neutrino_hierarchy='degenerate',
        num_massive_neutrinos=params['num_massive_neutrinos'],
        mnu=params['neutrino_mass'],
        standard_neutrino_neff=params['Neffective'],
        tau=params['tau'])

    A_s = 2e-9

    pars.set_dark_energy(
        w=params['w0'],
        wa=params['wa'])

    redshifts = [(1 / expfactor - 1)]
    if expfactor < 1:
        redshifts.append(0)

    pars.InitPower.set_params(ns=params['ns'], As=A_s)
    pars.YHe = 0.24
    pars.set_matter_power(
        redshifts=redshifts,
        kmax=kmax,
        k_per_logint=k_per_logint)

    pars.WantCls = False
    pars.WantScalars = False
    pars.Want_CMB = False
    pars.DoLensing = False

    # calculate results for these parameters
    results = camb.get_results(pars)

    index = 7 # cdm + baryons
    kh, z, pk = results.get_linear_matter_power_spectrum(var1=(1 + index),
                                                         var2=(1 + index),
                                                         hubble_units=True,
                                                         have_power_spectra=False,
                                                         params=None)
    pk = pk[-1, :]

    sigma8 = results.get_sigmaR(8, z_indices=-1, var1=(1 + index), var2=(1 + index))

    Normalization = (params['sigma8'] / sigma8)**2

    pk *= Normalization

    mask = (kh > 1e-4)

    return {'k': kh[mask], 'pk': pk[mask]}

class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def load_emu(emu_type='gp'):
    """Loads the emulator in memory.

    We don't automatize this step as -- at least for the gaussian process -- it
    loads approx 5.5 G in memory, and we don't want the user to do so accidentally.

    :param emu_type: type of emulator, can be 'gp' for the gaussian process, ot
                 'nn' for the neural network
    :type emu_type: str

    :return: a dictionary containing the emulator object
    :rtype: dict
    """
    import os
    if emu_type == 'gp':
        print('Loading emulator... (this can take up to one minute)')
    else:
        print('Loading emulator...')

    basefold = os.path.dirname(os.path.abspath(__file__))

    if emu_type == 'gp':
        old_names = [(basefold + '/' +
                      "gpy_emulator_data_iter3_big_120.pickle_fit_PCA8_sgnr_2_rot_vec.pkl"),
                      (basefold + '/' +
                      "gpy_emulator_data_iter4_big_160.pickle_fit_PCA5_sgnr_2_rot_bao_vec")
                    ]
        for old_name in old_names:
            if os.path.exists(old_name):
                os.remove(old_name)

        emulator_name = (basefold + '/' +
                        "gpy_emulator_data_iter4_big_160.pickle_fit_PCA6_sgnr_2_rot_bao_vec")

        if (not os.path.exists(emulator_name)) or (md5(emulator_name) != '7ec28f5f58a835448f2d787197db6a9e'):
            import urllib.request
            print('Downloading Emulator data (2Gb)...')
            urllib.request.urlretrieve(
                'http://bacco.dipc.org/gpy_emulator_data_iter4_big_160.pickle_fit_PCA6_sgnr_2_rot_bao_vec',
                emulator_name,
                MyProgressBar())

        emulator = {}
        with open(emulator_name, 'rb') as f:
            emulator['emulator'] = pickle.load(f)
            emulator['scaler'] = pickle.load(f)
            emulator['pca'] = pickle.load(f)
            emulator['k'] = pickle.load(f)
            emulator['components'] = pickle.load(f)
            emulator['rotation'] = pickle.load(f)
            emulator['bounds'] = pickle.load(f)
        emulator['emu_type'] = 'gp'
    elif emu_type == 'nn':
        from keras.models import load_model

        old_emulator_names = [(basefold + '/' +
                             "NN_emulator_data_iter4_big_160.pickle_sg_0.95_2000_rot_bao"),
                             (basefold + '/' +
                             "NN_emulator_data_iter4_big_160.pickle_sg_0.99_2000_PCA5_BNFalse_DO0rot_bao")]
        for old_emulator_name in old_emulator_names:
            if os.path.exists(old_emulator_name):
                import shutil
                shutil.rmtree(old_emulator_name)

        emulator_name = (basefold + '/' +
                         "NN_emulator_data_iter4_big_160.pickle_sg_0.99_2000_PCA6_BNFalse_DO0rot_bao")

        if (not os.path.exists(emulator_name)):
            import urllib.request
            import tarfile
            print('Downloading Emulator data (3Mb)...')
            urllib.request.urlretrieve(
                'http://bacco.dipc.org/NN_emulator_data_iter4_big_160.pickle_sg_0.99_2000_PCA6_BNFalse_DO0rot_bao.tar',
                emulator_name + '.tar',
                MyProgressBar())
            tf = tarfile.open(emulator_name+'.tar', 'r')
            tf.extractall(path=basefold)
            tf.close()
            os.remove(emulator_name + '.tar')
        emulator = {}
        emulator['emu_type'] = 'nn'
        emulator['model'] = load_model(emulator_name)
        with open(emulator_name + '/k_scaler_bounds.pkl', 'rb') as f:
            emulator['k'] = pickle.load(f)
            emulator['scaler'] = pickle.load(f)
            emulator['bounds'] = pickle.load(f)
    else:
        raise ValueError('Unrecognized emulator type {}, choose among gp and nn'.format(emu_type))
    print('Emulator loaded in memory.')
    return emulator


def eval_emu(coordinates, emulator=None):
    """Evaluate the given emulator at a set of coordinates in parameter space.

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param emulator: the emulator object, defaults to None
    :type emulator: dict, optional
    :return: the emulated value of Q(k) at this point in parameter space
    :rtype: array_like
    """
    pp = [
        coordinates['omega_matter'],
        coordinates['sigma8'],
        coordinates['omega_baryon'],
        coordinates['ns'],
        coordinates['hubble'],
        coordinates['neutrino_mass'],
        coordinates['w0'],
        coordinates['wa']
    ]
    pp = np.array([np.r_[pp, coordinates['expfactor']]])

    pname = ['omega_matter', 'sigma8', 'omega_baryon', 'ns', 'h',
             'neutrino_mass', 'w0', 'wa', 'expfactor']
    for i in range(len(pp[0])):
        message = 'Param {} out of bounds [{}, {}]'.format(
            pname[i], emulator['bounds'][i, 0], emulator['bounds'][i, 1])
        assert (pp[0, i] >= emulator['bounds'][i, 0]) & (pp[0, i] <= emulator['bounds'][i, 1]), message

    _pp = _transform_space(np.array(pp), space_rotation=False, bounds=emulator['bounds'])

    if emulator['emu_type'] == 'gp':
        npca = len(emulator['emulator'])
        cc = np.zeros(npca)
        for ii in range(npca):
            cc[ii], var = _bacco_evaluate_emulator(emulator=emulator['emulator'][ii], coordinates=_pp,
                                                gp_name='gpy')
        yrec = emulator['pca'].inverse_transform(cc)
        Q = np.exp(emulator['scaler'].inverse_transform(yrec))
    else:
        yrec = emulator['model'].predict(_pp)[0]
        Q = np.exp(emulator['scaler'].inverse_transform(yrec))

    _k, _pk_smeared = smeared_bao_pk(coordinates, k=emulator['k'])
    _k, _pk_lin = linear_pk(coordinates, k=emulator['k'])

    return Q * _pk_smeared / _pk_lin

def linear_pk(coordinates, k=None):
    """Compute the linear prediction of the cold matter power spectrum using camb

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param k: a vector of wavemodes in h/Mpc, if None the wavemodes used by
              camb are returned, defaults to None
    :type k: array_like, optional
    :return: k and linear pk
    :rtype: tuple
    """
    _pk_dict = _compute_camb_spectrum(coordinates)
    if k is not None:
        from scipy.interpolate import interp1d
        _k = k
        _interp = interp1d(np.log(_pk_dict['k']), np.log(_pk_dict['pk']), kind='cubic')
        _pk = np.exp(_interp(np.log(_k)))
    else:
        _k = _pk_dict['k']
        _pk = _pk_dict['pk']
    return _k, _pk

def nowiggles_pk(coordinates, k=None):
    """De-wiggled linear prediction of the cold matter power spectrum using camb

    The BAO feature is removed by identifying and removing its corresponding
    bump in real space, by means of a DST, and consequently transforming
    back to Fourier space.
    See:
    - Baumann et al 2018 (https://arxiv.org/pdf/1712.08067.pdf)
    - Giblin et al 2019 (https://arxiv.org/pdf/1906.02742.pdf)

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param k: a vector of wavemodes in h/Mpc, if None the wavemodes used by
              camb are returned, defaults to None
    :type k: array_like, optional
    :return: k and dewiggled pk
    :rtype: tuple
    """
    from scipy import interpolate
    from scipy.fftpack import dst, idst

    kcamb, pkcamb = linear_pk(coordinates, k=None)

    nk = int(2**15)
    kmin = kcamb.min()
    kmax = 10
    klin = np.linspace(kmin, kmax, nk)

    pkcamb_cs = interpolate.splrep(np.log(kcamb), np.log(pkcamb), s=0)
    pklin = np.exp(interpolate.splev(np.log(klin), pkcamb_cs, der=0, ext=0))

    f = np.log10(klin * pklin)

    dstpk = dst(f, type=2)

    even = dstpk[0::2]
    odd = dstpk[1::2]

    i_even = np.arange(len(even)).astype(int)
    i_odd = np.arange(len(odd)).astype(int)

    even_cs = interpolate.splrep(i_even, even, s=0)
    odd_cs = interpolate.splrep(i_odd, odd, s=0)

    even_2nd_der = interpolate.splev(i_even, even_cs, der=2, ext=0)
    odd_2nd_der = interpolate.splev(i_odd, odd_cs, der=2, ext=0)

    # these indexes have been fudged for the k-range considered
    # [~1e-4, 10], any other choice would require visual inspection
    imin_even = i_even[100:300][np.argmax(even_2nd_der[100:300])] - 20
    imax_even = i_even[100:300][np.argmin(even_2nd_der[100:300])] + 70
    imin_odd = i_odd[100:300][np.argmax(odd_2nd_der[100:300])] - 20
    imax_odd = i_odd[100:300][np.argmin(odd_2nd_der[100:300])] + 75

    i_even_holed = np.concatenate((i_even[:imin_even], i_even[imax_even:]))
    i_odd_holed = np.concatenate((i_odd[:imin_odd], i_odd[imax_odd:]))

    even_holed = np.concatenate((even[:imin_even], even[imax_even:]))
    odd_holed = np.concatenate((odd[:imin_odd], odd[imax_odd:]))

    even_holed_cs = interpolate.splrep(i_even_holed, even_holed * (i_even_holed+1)**2, s=0)
    odd_holed_cs = interpolate.splrep(i_odd_holed, odd_holed * (i_odd_holed+1)**2, s=0)

    even_smooth = interpolate.splev(i_even, even_holed_cs, der=0, ext=0) / (i_even + 1)**2
    odd_smooth = interpolate.splev(i_odd, odd_holed_cs, der=0, ext=0) / (i_odd + 1)**2

    dstpk_smooth = []
    for ii in range(len(i_even)):
        dstpk_smooth.append(even_smooth[ii])
        dstpk_smooth.append(odd_smooth[ii])
    dstpk_smooth = np.array(dstpk_smooth)

    pksmooth = idst(dstpk_smooth, type=2) / (2 * len(dstpk_smooth))
    pksmooth = 10**(pksmooth) / klin

    k_highk = kcamb[kcamb > 5]
    p_highk = pkcamb[kcamb > 5]

    k_extended = np.concatenate((klin[klin < 5], k_highk))
    p_extended = np.concatenate((pksmooth[klin < 5], p_highk))

    k = kcamb if k is None else k

    pksmooth_cs = interpolate.splrep(np.log(k_extended), np.log(p_extended), s=0)
    pksmooth_interp = np.exp(interpolate.splev(np.log(k), pksmooth_cs, der=0, ext=0))

    return k, pksmooth_interp

def smeared_bao_pk(coordinates, k=None):
    """Prediction of the cold matter power spectrum using camb with smeared BAO feature

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param k: a vector of wavemodes in h/Mpc, if None the wavemodes used by
              camb are returned, defaults to None
    :type k: array_like, optional
    :return: k and smeared BAO pk
    :rtype: tuple
    """
    from scipy.integrate import trapz

    k, pk_lin = linear_pk(coordinates, k=k)

    x, y = linear_pk(coordinates, k=None)
    y = x * y

    sigma_star_2 = trapz(y, x=np.log(x)) / (3 * np.pi**2)
    k_star_2 = 1 / sigma_star_2
    G = np.exp(-0.5 * (k**2 / k_star_2))
    _k, pk_nw = nowiggles_pk(coordinates, k=k)
    nl_pk = pk_lin * G + pk_nw * (1 - G)

    return k, nl_pk

def nonlinear_pk(coordinates, k=None, emulator=None):
    """Compute the prediction of the nonlinear cold matter power spectrum

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param k: a vector of wavemodes in h/Mpc, if None the wavemodes used to
              build the emulator are returned, defaults to None
    :type k: array_like, optional
    :param emulator: the emulator object, defaults to None
    :type emulator: obj, optional
    :return: k and nonlinear pk
    :rtype: tuple
    """
    Q = eval_emu(coordinates, emulator=emulator)
    if k is None:
        _k = emulator['k']
        _k, _pk_lin = linear_pk(coordinates, k=_k)
        _pk = Q * _pk_lin
    else:
        from scipy.interpolate import interp1d
        _k = k
        _k_emu, _pk_lin = linear_pk(coordinates, k=emulator['k'])
        _interp = interp1d(np.log(_k_emu), np.log(Q * _pk_lin), kind='cubic')
        _pk = np.exp(_interp(np.log(_k)))
    return _k, _pk
