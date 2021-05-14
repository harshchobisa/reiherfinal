mentors_filename="MentorSEAS Mentor Form.csv"
mentee_responses_filename="2020-21 MentorSEAS Mentee Form.csv"
mentees_master_filename="New-Freshmen.csv"

categoryChoices = {
    'ActivitiesRank': [
        'firstActivity',
        'secondActivity',
        'thirdActivity',
        'fourthActivity',
        'fifthActivity'],
    'Activities': [
        "Art/Theater",
        "Hiking/Outdoors",
        "Community Service",
        "Gym",
        "Greek Life",
        "Sports",
        "Video Games",
        "Watching TV/Movies",
        "Music" ],
    'MentorType': 'mentorType',
    'MenteeType': 'menteeType',
    'MentorTypeResponse': [
        'Academic',
        'Social'],
    'MenteeTypeResponse': [
        'Academic',
        'Social'],
    'MajorsQuestion': 'major',
    'Majors': [
        'Computer Science',
        'Computer Science and Engineering',
        'Computer Engineering',
        'Electrical Engineering',
        'Mechanical Engineering',
        'Aerospace Engineering',
        'Bioengineering',
        'Civil Engineering',
        'Materials Engineering',
        'Undeclared Engineering',
        'Chemical Engineering'],
}


# must strictly use numbers 1 through n
majorToNums = {
    'Aerospace Engineering': 2,
    'Bioengineering': 4,
    'Chemical Engineering': 3,
    'Civil Engineering': 3,
    'Computer Engineering': 1,
    'Computer Science': 1,
    'Computer Science and Engineering': 1,
    'Electrical Engineering': 1,
    'Materials Engineering': 3,
    'Mechanical Engineering': 2,
    'Undeclared Engineering': 4
}

# tied to the majorToNums, masterMajorToNums dict
num_major_categories = 4

mentorMatchCols = [
  categoryChoices.get('Activities')[0],
  categoryChoices.get('Activities')[1],
  categoryChoices.get('Activities')[2],
  categoryChoices.get('Activities')[3],
  categoryChoices.get('Activities')[4],
  categoryChoices.get('Activities')[5],
  categoryChoices.get('Activities')[6],
  categoryChoices.get('Activities')[7],
  categoryChoices.get('Activities')[8],
  categoryChoices.get('MajorsQuestion'),
  categoryChoices.get('MentorType')
]

menteeMatchCols = [
  categoryChoices.get('Activities')[0],
  categoryChoices.get('Activities')[1],
  categoryChoices.get('Activities')[2],
  categoryChoices.get('Activities')[3],
  categoryChoices.get('Activities')[4],
  categoryChoices.get('Activities')[5],
  categoryChoices.get('Activities')[6],
  categoryChoices.get('Activities')[7],
  categoryChoices.get('Activities')[8],
  categoryChoices.get('MajorsQuestion'),
  categoryChoices.get('MenteeType')
]


master_major_map={
  'AEROSPCE':'Aerospace Engineering',
  'BIOENGR':'Bioengineering',
  'CHM ENGR':'Chemical Engineering',
  'CIV ENGR':'Civil & Environmental Engineering',
  'COM ENGR':'Computer Engineering',
  'COM SCI':'Computer Science',
  'C S&ENGR':'Computer Science and Engineering',
  'ELE ENGR':'Electrical Engineering',
  'MAT ENGR':'Material Science and Engineering',
  'MECHANIC':'Mechanical Engineering',
  'UN-E&AS':'Undeclared Engineering'
}

