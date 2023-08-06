import numpy as np
import pandas as pd
import pytest
from joblib import Parallel, delayed
from sklearn.datasets import make_spd_matrix
from sklearn.decomposition import PCA

from precise.PRECISE import PRECISE


n_source_samples = 150
n_target_samples = 100
n_dimensions = 200
n_iter_spd_cov = 50
cov_sim_ratio = 0.9
n_jobs = 1
n_step = 10
n_iter_null = 20
n_pc = 20
n_pv = 15
rbf_params = {
    'gamma':1/n_dimensions
}

def generate_covariance_matrix():
    spd_matrices = Parallel(n_jobs=n_jobs, verbose=1)(delayed(make_spd_matrix)(n_dimensions) for _ in range(n_iter_spd_cov))
    return np.mean(spd_matrices, axis=0)


@pytest.fixture(scope='module')
def common_cov_matrix():
    return generate_covariance_matrix()


@pytest.fixture(scope='module')
def source_cov_matrix(common_cov_matrix):
    return cov_sim_ratio * common_cov_matrix + (1-cov_sim_ratio)*generate_covariance_matrix()


@pytest.fixture(scope='module')
def target_cov_matrix(common_cov_matrix):
    return cov_sim_ratio * common_cov_matrix + (1-cov_sim_ratio)*generate_covariance_matrix()


@pytest.fixture(scope='module')
def source_data(source_cov_matrix):
    X = np.random.multivariate_normal(mean=np.zeros(n_dimensions),
                                     cov=source_cov_matrix,
                                     size=n_source_samples)
    return X


@pytest.fixture(scope='module')
def source_data_centered(source_data):
    return source_data - np.mean(source_data, 0)


@pytest.fixture(scope='module')
def target_data(target_cov_matrix):
    X = np.random.multivariate_normal(mean=np.zeros(n_dimensions),
                                     cov=target_cov_matrix,
                                     size=n_target_samples)
    return X


class TestPRECISE():

    @pytest.fixture(scope='class')
    def linear_kernel_precise(self, source_data, target_data):

        linear_clf = PRECISE('linear', n_jobs=n_jobs)

        return linear_clf.fit(source_data,
                            target_data, 
                            n_components=n_pc,
                            n_pv=n_pv,
                            method='two-stage',
                            step=n_step)


    @pytest.fixture(scope='class')
    def linear_output_source(self, source_data, linear_kernel_precise):
        coef = np.random.randint(-10,10,size=linear_kernel_precise.principal_vectors_.n_pv)
        return linear_kernel_precise.transform(source_data).dot(coef)


    @pytest.fixture(scope='class')
    def linear_null_distribution(self, linear_kernel_precise):
        return linear_kernel_precise.null_distribution_pv_similarity(n_iter=n_iter_null)


    @pytest.fixture(scope='class')
    def rbf_kernel_precise(self, source_data, target_data):

        rbf_clf = PRECISE('rbf', kernel_params=rbf_params,  n_jobs=n_jobs)

        return rbf_clf.fit(source_data,
                        target_data, 
                        n_components=n_pc,
                        n_pv=n_pv,
                        method='two-stage',
                        step=n_step)


    def test_shape_and_values_linear(self,
                                linear_kernel_precise):
        
        assert linear_kernel_precise.optimal_time.shape == (n_pv,)
        for e in linear_kernel_precise.optimal_time:
            assert e >= 0
            assert e <= 1
        assert linear_kernel_precise.ks_statistics.shape == (n_pv, n_step+1)
        assert linear_kernel_precise.ks_p_values.shape == (n_pv, n_step+1)
        assert np.prod(linear_kernel_precise.ks_p_values >= 0)
        assert np.prod(linear_kernel_precise.ks_p_values <= 1)

        # Check that algo select time of maximal interpolation.
        for i in range(n_pv):
            assert np.prod(linear_kernel_precise.ks_statistics[i] >= 
                linear_kernel_precise.ks_statistics[i][int(linear_kernel_precise.optimal_time[i]*n_step)])

    def test_shape_and_values_rbf(self,
                                rbf_kernel_precise):
        
        assert rbf_kernel_precise.optimal_time.shape == (n_pv,)
        for e in rbf_kernel_precise.optimal_time:
            assert e >= 0
            assert e <= 1
        assert rbf_kernel_precise.ks_statistics.shape == (n_pv, n_step+1)
        assert rbf_kernel_precise.ks_p_values.shape == (n_pv, n_step+1)
        assert np.prod(rbf_kernel_precise.ks_p_values >= 0)
        assert np.prod(rbf_kernel_precise.ks_p_values <= 1)

        # Check that algo select time of maximal interpolation.
        for i in range(n_pv):
            assert np.prod(rbf_kernel_precise.ks_statistics[i] >= 
                rbf_kernel_precise.ks_statistics[i][int(rbf_kernel_precise.optimal_time[i]*n_step)])


    def test_shape_and_values_linear_transform(self,
                                            linear_kernel_precise,
                                            source_data,
                                            target_data):

        X_source = linear_kernel_precise.transform(source_data)
        X_target = linear_kernel_precise.transform(target_data)

        assert X_source.shape == (n_source_samples, n_pv)
        assert X_target.shape == (n_target_samples, n_pv)


    def test_shape_and_values_rbf_transform(self,
                                            rbf_kernel_precise,
                                            source_data,
                                            target_data):

        X_source = rbf_kernel_precise.transform(source_data)
        X_target = rbf_kernel_precise.transform(target_data)

        assert X_source.shape == (n_source_samples, n_pv)
        assert X_target.shape == (n_target_samples, n_pv)


    def test_shape_linear_null_distribution(self, linear_null_distribution):
        assert linear_null_distribution.shape == (n_iter_null, n_pv)
        # Test monotonicity
        for i in range(n_pv-1):
            assert np.prod(linear_null_distribution[:,i] >= linear_null_distribution[:,i+1])


    def test_prediction(self, source_data, linear_kernel_precise, linear_output_source):
        linear_kernel_precise.fit_predictor(source_data, linear_output_source)
        np.testing.assert_almost_equal(linear_output_source, linear_kernel_precise.predict(source_data))

    def test_prediction(self, source_data, linear_kernel_precise, linear_output_source):
        linear_kernel_precise.fit_predictor(source_data, linear_output_source)
        pred_perf = linear_kernel_precise.compute_pred_performance(source_data, linear_output_source, with_plot=True, cv=3)
        
        assert pred_perf[0] > 0.99
