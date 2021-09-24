import os
import unittest
import random
import shutil

import settings
from settings import get_full_path, get_full_file_path

from utils import (
    check_ids_correspond,
    get_files_and_ids,
    get_previous_ids,
    update_previous_id_database,
)


def cmp(a, b):
    # https://stackoverflow.com/questions/22490366/how-to-use-cmp-in-python-3
    return (a > b) - (a < b)


# unittest.TestLoader.sortTestMethodsUsing = None
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(y, x)


class TestUpdateDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.output_folder = get_full_path(os.path.join(".", "test_update_database"))
        self.output_file = get_full_file_path(
            self.output_folder, settings.database_of_extracted_pdfs,
        )
        self.populated_ids = None

        if os.listdir(self.output_folder):
            # https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
            for filename in os.listdir(self.output_folder):
                file_path = os.path.join(self.output_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))

        return super().setUp()

    def test_1_new_database(self):

        new_ids = [random.randint(1400000000, 1500000000) for _ in range(10)]

        self.assertFalse(os.path.exists(self.output_file))

        update_previous_id_database(self.output_file, new_ids)

        self.assertTrue(os.path.exists(self.output_file))

        previous_ids = get_previous_ids(self.output_file)

        self.assertEqual(set(previous_ids), set(new_ids))

        self.populated_ids = new_ids

    def test_2_append_database(self):

        self.assertTrue(os.path.exists(self.output_file))

        new_ids = [random.randint(1400000000, 1500000000) for _ in range(10)]
        settings.batch_number += 1

        update_previous_id_database(self.output_file, new_ids)
        ids_from_database = get_previous_ids(self.output_file)
        self.populated_ids.extend(new_ids)

        self.assertEqual(set(ids_from_database), set(self.populated_ids))


class TestIDCorrespondence(unittest.TestCase):
    def test_banner_target_no_database_not_cumulative(self):
        # suceeds
        # Should have same behaviour as if banner is not target
        path_to_files = get_full_path(
            os.path.join(".", "test_no_database_not_cumulative")
        )
        _, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = False

        settings.path_to_pdfs_to_extract = path_to_files
        settings.path_to_target_file = get_full_file_path(
            path_to_files, settings.target_ucas_id_file
        )
        settings.path_to_database_of_extracted_pdfs = get_full_file_path(
            path_to_files, settings.database_of_extracted_pdfs
        )

        correct_ids = {1462950865, 1461856964, 1483858362}
        solution = check_ids_correspond(applicant_ids)

        self.assertEqual(correct_ids, solution)

    def test_banner_target_no_database_is_cumulative(self):
        # same behaviour as previous
        # no database means it doesn't matter whether or not it is cumulative
        path_to_files = get_full_path(os.path.join(".", "test_no_database_cumulative"))
        _, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = False

        settings.path_to_pdfs_to_extract = path_to_files
        settings.path_to_target_file = get_full_file_path(
            path_to_files, settings.target_ucas_id_file
        )
        settings.path_to_database_of_extracted_pdfs = get_full_file_path(
            path_to_files, settings.database_of_extracted_pdfs
        )

        correct_ids = {1462950865, 1461856964, 1483858362}
        solution = check_ids_correspond(applicant_ids)

        self.assertEqual(correct_ids, solution)

    # def test_banner_target_with_database_not_cumulative(self):
    #     # suceeds
    #     path_to_files = get_full_path(
    #         os.path.join(".", "test_with_database_not_cumulative")
    #     )
    #     _, applicant_ids = get_files_and_ids(path_to_files)

    #     settings.is_id_file_banner = True
    #     settings.is_banner_cumulative = False

    #     settings.path_to_pdfs_to_extract = path_to_files
    #     settings.path_to_target_file = get_full_file_path(
    #         path_to_files, settings.target_ucas_id_file
    #     )
    #     settings.path_to_database_of_extracted_pdfs = get_full_file_path(
    #         path_to_files, settings.database_of_extracted_pdfs
    #     )

    #     correct_ids = {1462950865, 1461856964, 1483858362}
    #     solution = check_ids_correspond(applicant_ids)

    #     self.assertEqual(correct_ids, solution)


#     def banner_target_with_database_is_cumulative(self):
#         # suceeds
#         path_to_files = os.path.join(".", "test_with_database_cumulative")
#         all_files, applicant_ids = get_files_and_ids(path_to_files)

#         settings.is_id_file_banner = True
#         settings.is_banner_cumulative = True

#         settings.path_to_target_file = path_to_files
#         settings.path_to_database_of_extracted_pdfs = path_to_files
#         pass

# #     def banner_target_with_database_not_cumulative_fails(self):
# #         # failure situation
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)

# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def banner_target_with_database_is_cumulative_fails(self):
# #         # failure situation
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)

# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def id_only_target_succeeds(self):
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)

# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass


# # class TestFileIDCorrespondence(unittest.TestCase):
# #     def banner_target_no_database_not_cumulative(self):
# #         # suceeds
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)

# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def banner_target_no_database_is_cumulative(self):
# #         # determine behaviour
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)
# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def banner_target_with_database_not_cumulative(self):
# #         # suceeds
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)
# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def banner_target_with_database_is_cumulative(self):
# #         # suceeds
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)
# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def banner_target_with_database_not_cumulative_fails(self):
# #         # failure situation
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)
# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def banner_target_with_database_is_cumulative_fails(self):
# #         # failure situation
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)
# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass

# #     def id_only_target_succeeds(self):
# #         path_to_files = os.path.join(".", "a")
# #         all_files, applicant_ids = get_files_and_ids(path_to_files)
# #         settings.is_id_file_banner = True
# #         settings.is_banner_cumulative = True

# #         settings.path_to_target_file = path_to_files
# #         settings.path_to_database_of_extracted_pdfs = path_to_files
# #         pass


if __name__ == "__main__":
    unittest.main()
