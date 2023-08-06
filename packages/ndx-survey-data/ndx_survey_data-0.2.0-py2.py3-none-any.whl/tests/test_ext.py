
import numpy as np
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime
from ndx_survey_data import SurveyTable, QuestionResponse
from ndx_survey_data.survey_definitions import nrs_survey_table


def test_ext_nrs():

    nrs_survey_table.add_row(
        pain_intensity_rating=1.1,
        pain_relief_rating=5.5,
        relative_pain_intensity_rating=np.nan,
        pain_unpleasantness=np.nan,
        unix_timestamp=1588217283
    )

    nrs_survey_table.add_row(
        pain_intensity_rating=np.nan,
        pain_relief_rating=1,
        relative_pain_intensity_rating=6,
        pain_unpleasantness=2.7,
        unix_timestamp=1588217283
    )

    nrs_survey_table.add_row(
        pain_intensity_rating=5.3,
        pain_relief_rating=np.nan,
        relative_pain_intensity_rating=0.8,
        pain_unpleasantness=2.1,
        unix_timestamp=1588217283
    )

    nrs_survey_table.add_row(
        pain_intensity_rating=3.7,
        pain_relief_rating=np.nan,
        relative_pain_intensity_rating=6,
        pain_unpleasantness=np.nan,
        unix_timestamp=1588217283
    )

    nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

    nwbfile.create_processing_module(name='behavior', description='survey/behavioral data')

    nwbfile.processing['behavior'].add(nrs_survey_table)

    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()

        read_table = nwbfile.processing['behavior'].data_interfaces['nrs_survey_table'].to_dataframe()

    return np.testing.assert_array_equal(nrs_survey_table.to_dataframe(), read_table)


def test_ext_custom():

    q1 = QuestionResponse(name='question1',
                          description='desc',
                          options=['option 1', 'option 2', 'option 3'])

    q2 = QuestionResponse(name='question2',
                          description='desc',
                          options=['option 1', 'option 2', 'option 3'])

    q3 = QuestionResponse(name='question3',
                          description='desc',
                          options=['option 1', 'option 2', 'option 3'])

    custom_survey_table = SurveyTable(name='custom_survey_table',
                                      description='desc',
                                      columns=[q1, q2, q3])

    custom_survey_table.add_row(question1=1.3, question2=3.9, question3=0.2, unix_timestamp=1588217283)
    custom_survey_table.add_row(question1=3.3, question2=1.4, question3=0.6, unix_timestamp=1588217283)
    custom_survey_table.add_row(question1=2.5, question2=2.1, question3=2.8, unix_timestamp=1588217283)

    nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

    nwbfile.create_processing_module(name='behavior', description='survey/behavioral data')

    nwbfile.processing['behavior'].add(custom_survey_table)

    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()

        read_table = nwbfile.processing['behavior'].data_interfaces['custom_survey_table'].to_dataframe()

    return np.testing.assert_array_equal(custom_survey_table.to_dataframe(), read_table)
