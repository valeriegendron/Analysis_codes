####
import numpy as np

galaxy_name = 'Af_v1'
# fileName = "s000062"

sfileNames1 = ["s000005", "s000007", "s000010", "s000013", "s000016", "s000019"]
sfileNames2 = ["s000021", "s000023"]
sfileNames3 = ["s000040"]
sfileNames4 = ["s000046", "s000051", "s000057", "s000062", "s000066", "s000071", "s000075", "s000080", "s000084"]
sfileNames5 = ["s000103", "s000107"]
sfileNames6 = ["s000110", "s000114", "s000118", "s000122", "s000127", "s000130"]

gfileNames1 = ["g000000", "g000005", "g000007", "g000010", "g000013", "g000016", "g000019"]
gfileNames2 = ["g000021", "g000023"]


# STARS
for fileName in sfileNames1:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19,\
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c0[i] < 0.10:  # if x < 10 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19,\
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29 = [], [], [], [], [], [], [], [], [], [],\
                                                           [], [], [], [], [], [], [], [], [], [],\
                                                           [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E'*19 + '%10d'*2 + '%13.5E'*9)

for fileName in sfileNames2:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c2[i] < 0.05:  # if z < 5 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29 = [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E'*19 + '%10d'*2 + '%13.5E'*9)

for fileName in sfileNames3:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c0[i] > -0.05:  # if x > -5 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29 = [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E'*19 + '%10d'*2 + '%13.5E'*9)

for fileName in sfileNames4:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c0[i] > -0.08:  # if x > -8 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29 = [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E'*19 + '%10d'*2 + '%13.5E'*9)

for fileName in sfileNames5:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c0[i] < 0.08:  # if x < 8 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29 = [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E'*19 + '%10d'*2 + '%13.5E'*9)

for fileName in sfileNames6:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c2[i] > -0.05:  # if x < 10 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29 = [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], [], \
                                                       [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E'*19 + '%10d'*2 + '%13.5E'*9)

# GAS
for fileName in gfileNames1:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c34, c35, c36, c37,\
        c38, c39, c40 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c0[i] < 0.10:  # if x < 10 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37,\
        t38, t39, t40 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
                        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29',
              'c30', 'c31', 'c32', 'c33', 'c34', 'c35', 'c36', 'c37', 'c38', 'c39', 'c40']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29',
              't30', 't31', 't32', 't33', 't34', 't35', 't36', 't37', 't38', 't39', 't40']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29,
                            t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E' * 18 + '%10d' * 2 + '%13.5E' * 19 + '%10d' * 2)

for fileName in gfileNames2:
    # Read star file
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, \
        c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c34, c35, c36, c37,\
        c38, c39, c40 = np.loadtxt(str(galaxy_name) + "/" + fileName, unpack=True)

    target_index = []
    impactor_index = []
    for i in range(0, len(c0)):
        if c2[i] < 0.05:  # if x < 5 kpc: target galaxy
            target_index.append(i)

    # Initialization for target galaxy data
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, \
        t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37,\
        t38, t39, t40 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], \
                        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    # Lists for loop
    c_list = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14',
              'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29',
              'c30', 'c31', 'c32', 'c33', 'c34', 'c35', 'c36', 'c37', 'c38', 'c39', 'c40']
    # target galaxy
    t_list = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
              't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29',
              't30', 't31', 't32', 't33', 't34', 't35', 't36', 't37', 't38', 't39', 't40']

    for index in target_index:
        for column in range(0, len(c_list)):
            (locals()[t_list[column]]).append(locals()[c_list[column]][index])
            # t0.append(c0[index])

    data = np.column_stack([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
                            t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29,
                            t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40])

    # Sauvegarde des données
    datafile_path = str(galaxy_name) + '/data_target/' + str(fileName)
    np.savetxt(datafile_path, data, fmt='%13.5E' * 18 + '%10d' * 2 + '%13.5E' * 19 + '%10d' * 2)
