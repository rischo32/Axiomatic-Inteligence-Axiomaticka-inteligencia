from scipy.stats import beta

def bayes_update_weight(prior_a, prior_b, new_data_success, new_data_trials):
    posterior_a = prior_a + new_data_success
    posterior_b = prior_b + (new_data_trials - new_data_success)
    return beta.mean(posterior_a, posterior_b)

# Príklad: Prior Beta(1,1) = uniform, 8 úspechov z 10 pokusov
updated_weight = bayes_update_weight(1, 1, 8, 10)
print(f"Updated weight: {updated_weight:.4f}")
