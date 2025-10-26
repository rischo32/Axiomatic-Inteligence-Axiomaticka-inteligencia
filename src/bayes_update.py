# scripts/bayes_update.py
from scipy.stats import beta

def bayes_update_weight(prior_a, prior_b, new_data_success, new_data_trials):
    posterior_a = prior_a + new_data_success
    posterior_b = prior_b + (new_data_trials - new_data_success)
    return beta.mean(posterior_a, posterior_b)

if __name__ == '__main__':
    # example
    updated = bayes_update_weight(1,1,8,10)
    print("Updated weight:", updated)
