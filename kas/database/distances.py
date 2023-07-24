DISTANCES_INSIDE_CITY = {
    '1': 14, '2': 4, '3': 20, '4': 35, '5': 16,
    '7': 21, '8': 10, '9': 37, '10': 15, '11': 22, '12': 9, '13': 50,
    '14': 33, '15': 15, '17': 36, '18': 9, '19': 27, '20': 31,
    '200': 45, '21': 37, '22': 17, '23': 11, '24': 18, '25': 26,
    '26': 14, '27': 18, '28': 14, '30': 36, '31': 15
}

DISTANCES_OUTSIDE_CITY = {
    '6': 133, '16': 211, '217': 180, '264': 185, '265': 182,
    '229': 148, '231': 145, '230': 35, '237': 224, '238': 220,
    '235': 280, '248': 194, '239': 252, '247': 130, '201': 135,
    '263': 130, '249': 400, '243': 390, '220': 277, '222': 231,
    '219': 232, '221': 239, '245': 243, '224': 31, '223': 151,
    '225': 195, '212': 93, '227': 94, '228': 97, '213': 139,
    '214': 138, '262': 145, '232': 202, '233': 204,
}

DIST_STATIONS_INSIDE = [
    {

        '1': {
            '2': 21, '3': 22, '4': 24, '5': 10,
            '7': 21, '8': 21, '9': 45, '10': 14, '11': 16, '12': 28,
            '13': 54, '14': 50, '15': 39, '17': 30, '18': 45, '19': 50,
            '20': 25, '200': 50, '21': 37, '22': 6, '23': 18, '24': 7,
            '25': 35, '26': 12, '27': 10, '28': 9, '30': 40
        },
        '2': {
            '1': 21, '3': 15, '4': 27, '5': 21, '7': 22,
            '8': 8, '9': 33, '10': 14, '11': 24, '12': 7, '13': 45,
            '14': 22, '15': 20, '17': 30, '18': 20, '19': 25, '20': 40,
            '200': 33, '21': 34, '22': 21, '23': 10, '24': 16, '25': 30,
            '26': 12, '27': 12, '28': 10, '30': 32
        },
        '3': {
            '1': 22, '3': 15, '4': 42, '5': 34, '7': 37,
            '8': 18, '9': 24, '10': 7, '11': 36, '12': 9, '13': 73, '14': 31,
            '15': 60, '17': 50, '18': 40, '19': 45, '20': 45, '200': 65,
            '21': 51, '22': 18, '23': 8, '24': 13, '25': 50, '26': 16,
            '27': 13, '28': 11, '30': 55
        },
        '4': {
            '1': 24, '2': 27, '3': 42, '5': 20, '7': 9,
            '8': 33, '9': 62, '10': 40, '11': 9, '12': 41, '13': 40, '14': 74,
            '15': 27, '17': 12, '18': 17, '19': 23, '20': 30, '200': 31,
            '21': 13, '22': 24, '23': 47, '24': 34, '25': 13, '26': 37,
            '27': 37, '28': 36, '30': 20
        },
        '5': {
            '1': 10, '2': 21, '3': 34, '4': 20, '7': 9,
            '8': 24, '9': 58, '10': 18, '11': 8, '12': 23, '13': 67, '14': 58,
            '15': 29, '17': 35, '18': 30, '19': 37, '20': 18, '200': 42,
            '21': 29, '22': 11, '23': 34, '24': 21, '25': 30, '26': 11,
            '27': 15, '28': 14, '30': 33
        },
        '7': {
            '1': 21, '2': 22, '3': 37, '4': 9, '5': 9,
            '8': 5,
            '9': 61, '10': 29, '11': 7, '12': 27, '13': 51, '14': 66, '15': 25,
            '17': 21, '18': 25, '19': 32, '20': 17, '200': 36, '21': 23,
            '22': 14, '23': 38, '24': 25, '25': 20, '26': 26, '27': 25,
            '28': 24, '30': 25
        },
        '8': {
            '1': 21, '2': 8, '3': 18, '4': 33, '5': 24,
            '7': 28,
            '9': 35, '10': 21, '11': 28, '12': 9, '13': 57, '14': 19, '15': 30,
            '17': 40, '18': 25, '19': 30, '20': 41, '200': 42, '21': 39,
            '22': 23,
            '23': 18, '24': 18, '25': 35, '26': 15, '27': 15, '28': 12,
            '30': 40
        },
        '9': {
            '1': 45, '2': 33, '3': 24, '4': 62, '5': 58,
            '7': 61,
            '8': 35, '10': 31, '11': 60, '12': 27, '13': 86, '14': 34,
            '15': 93,
            '17': 70, '18': 55, '19': 60, '20': 61, '200': 85, '21': 72,
            '22': 41,
            '23': 21, '24': 34, '25': 70, '26': 36, '27': 33, '28': 31,
            '30': 75
        },
        '10': {
            '1': 14, '2': 14, '3': 7, '4': 40, '5': 18,
            '7': 29,
            '8': 21, '9': 31, '11': 30, '12': 12, '13': 65, '14': 36, '15': 40,
            '17': 30, '18': 45, '19': 50, '20': 39, '200': 61, '21': 50,
            '22': 17,
            '23': 9, '24': 12, '25': 48, '26': 9, '27': 6, '28': 5, '30': 52
        },
        '11': {
            '1': 16, '2': 24, '3': 36, '4': 9, '5': 8,
            '7': 7,
            '8': 28, '9': 60, '10': 30, '12': 35, '13': 50, '14': 70, '15': 20,
            '17': 15, '18': 25, '19': 35, '20': 18, '200': 33, '21': 17,
            '22': 15,
            '23': 42, '24': 30, '25': 19, '26': 30, '27': 30, '28': 29,
            '30': 25
        },
        '12': {
            '1': 28, '2': 7, '3': 9, '4': 41, '5': 23,
            '7': 27,
            '8': 9, '9': 27, '10': 12, '11': 35, '13': 78, '14': 35, '15': 62,
            '17': 50, '18': 25, '19': 40, '20': 50, '200': 44, '21': 53,
            '22': 21,
            '23': 3, '24': 15, '25': 51, '26': 11, '27': 11, '28': 9, '30': 37
        },
        '13': {
            '1': 62, '2': 53, '3': 41, '4': 67, '5': 51,
            '7': 57,
            '8': 78, '9': 65, '10': 50, '11': 78, '12': 75, '14': 33, '15': 48,
            '17': 43, '18': 33, '19': 24, '20': 54, '200': 12, '21': 50,
            '22': 55,
            '23': 79, '24': 66, '25': 28, '26': 65, '27': 66, '28': 66,
            '30': 28
        },
        '14': {
            '1': 50, '2': 22, '3': 31, '4': 50, '5': 58,
            '7': 66, '8': 19, '9': 34, '10': 36, '11': 70, '12': 35, '13': 75,
            '15': 93, '17': 80, '18': 45, '19': 50, '20': 57, '200': 93,
            '21': 80,
            '22': 49, '23': 31, '24': 42, '25': 75, '26': 42, '27': 40,
            '28': 40, '30': 53
        },
        '15': {
            '1': 39, '2': 20, '3': 60, '4': 27, '5': 29,
            '7': 25,
            '8': 30, '9': 93, '10': 40, '11': 20, '12': 62, '13': 33, '14': 93,
            '17': 20, '18': 20, '19': 5, '20': 35, '200': 20, '21': 30,
            '22': 34,
            '23': 24, '24': 42, '25': 19, '26': 24, '27': 24, '28': 40,
            '30': 25
        },
        '17': {
            '1': 30, '2': 30, '3': 50, '4': 12, '5': 35,
            '7': 21,
            '8': 40, '9': 70, '10': 30, '11': 15, '12': 50, '13': 48, '14': 80,
            '15': 20, '18': 22, '19': 21, '20': 40, '200': 34, '21': 7,
            '22': 28,
            '23': 52, '24': 49, '25': 19, '26': 38, '27': 40, '28': 40,
            '30': 17
        },
        '18': {
            '1': 45, '2': 20, '3': 40, '4': 17, '5': 30,
            '7': 25,
            '8': 25, '9': 55, '10': 45, '11': 25, '12': 25, '13': 43, '14': 45,
            '15': 20, '17': 22, '19': 5, '20': 47, '200': 27, '21': 30,
            '22': 18,
            '23': 20, '24': 23, '25': 23, '26': 19, '27': 19, '28': 17,
            '30': 26
        },
        '19': {
            '1': 50, '2': 25, '3': 45, '4': 23, '5': 37,
            '7': 32,
            '8': 30, '9': 60, '10': 50, '11': 35, '12': 40, '13': 33, '14': 50,
            '15': 5, '17': 21, '18': 5, '20': 23, '200': 18, '21': 28,
            '22': 33,
            '23': 25, '24': 44, '25': 22, '26': 43, '27': 24, '28': 22,
            '30': 23
        },
        '20': {
            '1': 25, '2': 40, '3': 45, '4': 30, '5': 18,
            '7': 17, '8': 41, '9': 61, '10': 39, '11': 18, '12': 50, '13': 54,
            '14': 57, '15': 35, '17': 40, '18': 47, '19': 23, '200': 49,
            '21': 32, '22': 26, '23': 40, '24': 27, '25': 35, '26': 26,
            '27': 27, '28': 27, '30': 47

        },
        '200': {
            '1': 50, '2': 33, '3': 65, '4': 31, '5': 42,
            '7': 36, '8': 42, '9': 85, '10': 61, '11': 33, '12': 44, '13': 12,
            '14': 93, '15': 20, '17': 34, '18': 27, '19': 18, '20': 49,
            '21': 31, '22': 45, '23': 70, '24': 55, '25': 17, '26': 54,
            '27': 56, '28': 55, '30': 17
        },
        '21': {
            '1': 37, '2': 34, '3': 51, '4': 13, '5': 29,
            '7': 23, '8': 39, '9': 72, '10': 50, '11': 17, '12': 53, '13': 50,
            '14': 80, '15': 30, '17': 7, '18': 30, '19': 28, '20': 32,
            '200': 35, '22': 35, '23': 60, '24': 46, '25': 25, '26': 45,
            '27': 46, '28': 45, '30': 18
        },
        '22': {
            '1': 6, '2': 21, '3': 18, '4': 24, '5': 11,
            '7': 14, '8': 23, '9': 41, '10': 17, '11': 15, '12': 21, '13': 55,
            '14': 49, '15': 34, '17': 28, '18': 18, '19': 33, '20': 26,
            '200': 45, '21': 35, '23': 27, '24': 14, '25': 34, '26': 13,
            '27': 15, '28': 15, '30': 40
        },
        '23': {
            '1': 18, '2': 10, '3': 8, '4': 47, '5': 34,
            '7': 38, '8': 8, '9': 21, '10': 9, '11': 42, '12': 3, '13': 79,
            '14': 31, '15': 24, '17': 52, '18': 20, '19': 25, '20': 40,
            '200': 70, '21': 60, '22': 27, '24': 20, '25': 53, '26': 15,
            '27': 15, '28': 13, '30': 40
        },
        '24': {
            '1': 7, '2': 16, '3': 13, '4': 34, '5': 21,
            '7': 25, '8': 18, '9': 34, '10': 12, '11': 30, '12': 15, '13': 66,
            '14': 42, '15': 42, '17': 49, '18': 23, '19': 44, '20': 27,
            '200': 55, '21': 46, '22': 14, '23': 20, '25': 40, '26': 10,
            '27': 11, '28': 10, '30': 45
        },
        '25': {
            '1': 35, '2': 30, '3': 50, '4': 13, '5': 30,
            '7': 20, '8': 35, '9': 70, '10': 48, '11': 19, '12': 51, '13': 28,
            '14': 75, '15': 19, '17': 19, '18': 23, '19': 22, '20': 35,
            '200': 17, '21': 25, '22': 34, '23': 53, '24': 40, '26': 40,
            '27': 40, '28': 40, '30': 5
        },
        '26': {
            '1': 12, '2': 12, '3': 16, '4': 37, '5': 11,
            '7': 26, '8': 15, '9': 36, '10': 9, '11': 30, '12': 11, '13': 65,
            '14': 42, '15': 24, '17': 38, '18': 19, '19': 43, '20': 26,
            '200': 54, '21': 45, '22': 13, '23': 15, '24': 10, '25': 40,
            '27': 10, '28': 4, '30': 45
        },
        '27': {
            '1': 10, '2': 12, '3': 13, '4': 37, '5': 15,
            '7': 25, '8': 15, '9': 33, '10': 6, '11': 30, '12': 11, '13': 66,
            '14': 40, '15': 24, '17': 40, '18': 19, '19': 24, '20': 27,
            '200': 56, '21': 46, '22': 15, '23': 15, '24': 11, '25': 40,
            '26': 10, '28': 7, '30': 47
        },
        '28': {
            '1': 9, '2': 10, '3': 11, '4': 36, '5': 14,
            '7': 24, '8': 12, '9': 31, '10': 5, '11': 29, '12': 9, '13': 66,
            '14': 40, '15': 40, '17': 40, '18': 17, '19': 22, '20': 27,
            '200': 55, '21': 45, '22': 15, '23': 13, '24': 10, '25': 40,
            '26': 4, '27': 7, '30': 50
        },
        '30': {
            '1': 40, '2': 32, '3': 55, '4': 20, '5': 33,
            '7': 25, '8': 40, '9': 75, '10': 52, '11': 25, '12': 37,
            '13': 28, '14': 53, '15': 25, '17': 17, '18': 26, '19': 23,
            '20': 47, '200': 17, '21': 18, '22': 40, '23': 40, '24': 45,
            '25': 5, '26': 45, '27': 47, '28': 50
        }
    }
]
