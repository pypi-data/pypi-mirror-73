from sklearn.linear_model import LinearRegression

from sklearn.linear_model import Ridge

from sklearn.linear_model import Lasso

from sklearn.svm import SVR

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import RandomForestRegressor

from sklearn.ensemble import AdaBoostRegressor


def linearreg(copy_X,fit_intercept,n_jobs,normalize):
  
    return LinearRegression(copy_X,fit_intercept,n_jobs,normalize)


def ridge(alpha,copy_X,fit_intercept,max_iter,normalize,random_state,solver,tol):
    return Ridge(alpha,copy_X,fit_intercept,max_iter,normalize,random_state,solver,tol)


def lasso(alpha,copy_X,fit_intercept,max_iter,normalize,positive,precompute,random_state,selection,tol,warm_start):
    return Lasso(alpha,copy_X,fit_intercept,max_iter,normalize,positive,precompute,random_state,selection,tol,warm_start)


def supportv(C,cache_size,coef0,degree,epsilon,gamma,kernel,max_iter,shrinking,tol,verbose):
    return SVR(C,cache_size,coef0,degree,epsilon,gamma,kernel,max_iter,shrinking,tol,verbose)


def dtree(ccp_alpha,criterion,max_depth,max_features,max_leaf_nodes,min_impurity_decrease,min_impurity_split,min_samples_leaf,min_samples_split,min_weight_fraction_leaf,presort,random_state,splitter):
    return DecisionTreeRegressor(ccp_alpha,criterion,max_depth,max_features,max_leaf_nodes,min_impurity_decrease,min_impurity_split,min_samples_leaf,min_samples_split,min_weight_fraction_leaf,presort,random_state,splitter)

def randtree(bootstrap,ccp_alpha,criterion,max_depth,max_features,max_leaf_nodes,max_samples,min_impurity_decrease,min_impurity_split,min_samples_leaf,min_samples_split,min_weight_fraction_leaf,n_estimators,n_jobs,oob_score,random_state,verbose,warm_start):
    return RandomForestRegressor(bootstrap,ccp_alpha,criterion,max_depth,max_features,max_leaf_nodes,max_samples,min_impurity_decrease,min_impurity_split,min_samples_leaf,min_samples_split,min_weight_fraction_leaf,n_estimators,n_jobs,oob_score,random_state,verbose,warm_start)


def adboost(base_estimator, n_estimator, learning_rate, loss, random_state):
    return AdaBoostRegressor(base_estimator, n_estimator, learning_rate, loss, random_state)
