# Bulk create Moodle courses

Use this script to create a csv upload for courses and users into those courses. This is useful in cases where you are running a Moodle workshop and want to generate sandbox courses for everyone.

The input csv must contain the following fields:

* email
* firstname
* lastname

Optionally, if you know your user's Moodle usernames you can also include `username`.

## Usage


	positional arguments:
	users                 CSV containing user information
	course_name_prefix    Prefix attached to generated course names
	category              The moodle category ID these courses are created in

	optional arguments:
	--generate-passwords  Generate usernames and passwords in CSV if you are
                          also generating user accounts at the same time


The script generates two output files, `courses.csv` and `enroll.csv`. `courses.csv` can be uploaded using Moodle's [upload courses](https://docs.moodle.org/38/en/Upload_courses) function. `enroll.csv` can be uploaded using Moodle's [upload users](https://docs.moodle.org/38/en/Upload_users) function.

`courses.csv` **must** be uploaded first so that the courses exist when you upload `enroll.csv`