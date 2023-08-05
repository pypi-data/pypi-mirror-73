__all__ = ['calculate_stimulus_delivered']

# Find out tao for decay and membrane change?
def calculate_stimulus_delivered(stimulation_mode='phasic', stimulation_duration=6, interburst_duration=16,
                                 stimulation_frequency=15, number_of_stimulations=10):
    """A quick utility function to calculate the number of stimulus delivered over the course of a train of stims

    :param stimulation_mode: str, options: 'phasic', 'tonic'; mode of stimulation
    :param stimulation_duration: float, time in seconds of stimulation
    :param interburst_duration: float, time in seconds from start of stim 0 to start of stim 1
    :param stimulation_frequency: int, rate of stimulation
    :param number_of_stimulations: int, number of stimulation pulses

    :return: number of stimulations, time course of stims
    """
    if stimulation_mode.lower() == 'tonic':
        stim_amount = stimulation_duration * stimulation_frequency
        start_to_end = stimulation_duration

    if stimulation_mode.lower() == 'phasic':
        stim_amount =  stimulation_duration * stimulation_frequency * number_of_stimulations
        start_to_end = interburst_duration * number_of_stimulations

    return stim_amount, start_to_end


if __name__ == '__main__':
    a,b = calculate_stimulus_delivered(stimulation_mode='phasic',
                                       stimulation_duration=6,
                                       interburst_duration=16,
                                       stimulation_frequency=15,
                                       number_of_stimulations=10)
    print('15 Hz 10 stim 6s', a, b)

    a, b = calculate_stimulus_delivered(stimulation_mode='phasic',
                                        stimulation_duration=6,
                                        interburst_duration=16,
                                        stimulation_frequency=15,
                                        number_of_stimulations=5)
    print('15 Hz 5 stim 6s', a, b)

    a, b = calculate_stimulus_delivered(stimulation_mode='phasic',
                                        stimulation_duration=6,
                                        interburst_duration=16,
                                        stimulation_frequency=20,
                                        number_of_stimulations=5)
    print('20 Hz 5 stim 6s', a, b)

    a, b = calculate_stimulus_delivered(stimulation_mode='phasic',
                                        stimulation_duration=7,
                                        interburst_duration=16,
                                        stimulation_frequency=20,
                                        number_of_stimulations=5)
    print('20 Hz 5 stim 7s', a, b)

    a, b = calculate_stimulus_delivered(stimulation_mode='phasic',
                                        stimulation_duration=6,
                                        interburst_duration=16,
                                        stimulation_frequency=15,
                                        number_of_stimulations=7)
    print('15 Hz 7 stim 6s', a, b)

    a, b = calculate_stimulus_delivered(stimulation_mode='phasic',
                                        stimulation_duration=7,
                                        interburst_duration=16,
                                        stimulation_frequency=15,
                                        number_of_stimulations=5)
    print('15 Hz 5 stim 7s', a, b)
