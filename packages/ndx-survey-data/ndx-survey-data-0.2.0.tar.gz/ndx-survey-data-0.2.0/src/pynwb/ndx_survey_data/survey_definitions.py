from .survey_data import QuestionResponse, SurveyTable

# define NRS table
nrs_pain_intensity_rating = QuestionResponse(name='pain_intensity_rating',
                                             description='desc',
                                             options=['0.0 (no pain)', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0',
                                                      '8.0', '9.0', '10.0 (worst pain)'])

nrs_pain_relief_rating = QuestionResponse(name='pain_relief_rating',
                                          description='desc',
                                          options=['0.0 (no pain relief)', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0',
                                                   '7.0', '8.0', '9.0', '10.0 (complete pain relief)'])

nrs_relative_pain_intensity_rating = QuestionResponse(name='relative_pain_intensity_rating',
                                                      description='desc',
                                                      options=['0.0 (better)', '1.0', '2.0', '3.0', '4.0', '5.0 (same)',
                                                               '6.0', '7.0', '8.0', '9.0', '10.0 (worse)'])

nrs_pain_unpleasantness = QuestionResponse(name='pain_unpleasantness',
                                           description='desc',
                                           options=['0.0 (pleasant)', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0',
                                                    '8.0', '9.0', '10.0 (unpleasant)'])

nrs_survey_table = SurveyTable(name='nrs_survey_table',
                               description='desc',
                               columns=[
                                   nrs_pain_intensity_rating,
                                   nrs_pain_relief_rating,
                                   nrs_relative_pain_intensity_rating,
                                   nrs_pain_unpleasantness
                               ])

# define VAS table

vas_pain_intensity_rating = QuestionResponse(name='pain_intensity_rating',
                                             description='desc',
                                             options=['0.0 (No pain)'] + [str(float(i)) for i in range(2, 100)] + ['100.0 (Worst pain possible)'])

vas_pain_relief_rating = QuestionResponse(name='pain_relief_rating',
                                          description='desc',
                                          options=['0.0 (no pain relief)'] + [str(float(i)) for i in range(2, 100)] + ['100.0 (complete pain relief)'])

vas_relative_pain_intensity_rating = QuestionResponse(name='relative_pain_intensity_rating',
                                                      description='desc',
                                                      options=['0.0 (better)'] + [str(float(i)) for i in range(2, 100)] + ['100.0 (worse)'])

vas_pain_unpleasantness = QuestionResponse(name='pain_unpleasantness',
                                           description='desc',
                                           options=['0.0 (pleasant)'] + [str(float(i)) for i in range(2, 100)] + ['100.0 (unpleasant)'])

vas_survey_table = SurveyTable(name='vas_survey_table',
                               description='desc',
                               columns=[
                                   vas_pain_intensity_rating,
                                   vas_pain_relief_rating,
                                   vas_relative_pain_intensity_rating,
                                   vas_pain_unpleasantness
                               ])

# define MPQ table

mpq_options = ['Mild', 'Moderate', 'Severe']

throbbing = QuestionResponse(name='throbbing',
                             description='desc',
                             options=mpq_options)

shooting = QuestionResponse(name='shooting',
                            description='desc',
                            options=mpq_options)

stabbing = QuestionResponse(name='stabbing',
                            description='desc',
                            options=mpq_options)

sharp = QuestionResponse(name='sharp',
                         description='desc',
                         options=mpq_options)

cramping = QuestionResponse(name='cramping',
                            description='desc',
                            options=mpq_options)

gnawing = QuestionResponse(name='gnawing',
                           description='desc',
                           options=mpq_options)

hot_burning = QuestionResponse(name='hot_burning',
                               description='desc',
                               options=mpq_options)

aching = QuestionResponse(name='aching',
                          description='desc',
                          options=mpq_options)

heavy = QuestionResponse(name='heavy',
                         description='desc',
                         options=mpq_options)

tender = QuestionResponse(name='tender',
                          description='desc',
                          options=mpq_options)

splitting = QuestionResponse(name='splitting',
                             description='desc',
                             options=mpq_options)

tiring_exhausting = QuestionResponse(name='tiring_exhausting',
                                     description='desc',
                                     options=mpq_options)

sickening = QuestionResponse(name='sickening',
                             description='desc',
                             options=mpq_options)

fearful = QuestionResponse(name='fearful',
                           description='desc',
                           options=mpq_options)

cruel_punishing = QuestionResponse(name='cruel_punishing',
                                   description='desc',
                                   options=mpq_options)

mpq_survey_table = SurveyTable(name='mpq_survey_table',
                               description='desc',
                               columns=[
                                   throbbing,
                                   shooting,
                                   stabbing,
                                   sharp,
                                   cramping,
                                   gnawing,
                                   hot_burning,
                                   aching,
                                   heavy,
                                   tender,
                                   splitting,
                                   tiring_exhausting,
                                   sickening,
                                   fearful,
                                   cruel_punishing
                               ])
