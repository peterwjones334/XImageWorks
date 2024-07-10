from filters_basic import basic_effects
from filters_artistic import artistic_effects
from filters_noise import noise_effects
from filters_custom import custom_effects

# Aggregate all effects
effects = {}
effects.update(basic_effects)
effects.update(artistic_effects)
effects.update(noise_effects)
effects.update(custom_effects)

# Optionally add additional effects directly here if needed
