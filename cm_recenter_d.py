import numpy as np
import os

galaxy_name = 'I'
# Files
for fileName in os.listdir(str(galaxy_name)):
    if fileName.startswith("d00"):
        columns = (0, 1, 2, 3, 4, 5, 6)  # x, y, z, v_x, v_y, v_z et masse de la particule

        # Lecture des donnees
        x, y, z, v_x, v_y, v_z, mass = np.loadtxt(str(galaxy_name)+"/"+str(fileName), usecols=columns, unpack=True)

        # Calcul du centre de masse
        mx, my, mz, mv_x, mv_y, mv_z, m_tot = 0, 0, 0, 0, 0, 0, 0
        for i in range(0, len(x)):
            mx += mass[i]*x[i]
            my += mass[i]*y[i]
            mz += mass[i]*z[i]
            mv_x += mass[i]*v_x[i]
            mv_y += mass[i]*v_y[i]
            mv_z += mass[i]*v_z[i]
            m_tot += mass[i]

        x_cm, y_cm, z_cm = mx/m_tot, my/m_tot, mz/m_tot
        v_x_cm, v_y_cm, v_z_cm = mv_x/m_tot, mv_y/m_tot, mv_z/m_tot

        # Correction des coordonnees des particules
        for i in range(0, len(x)):
            x[i] = x[i]-x_cm
            y[i] = y[i]-y_cm
            z[i] = z[i]-z_cm
            v_x[i] = v_x[i]-v_x_cm
            v_y[i] = v_y[i]-v_y_cm
            v_z[i] = v_z[i]-v_z_cm

        # Ecriture dans un nouveau fichier
        # Lecture des autres donnees à ajouter au nouveau fichier
        columns2 = (7, 8, 9, 10, 11, 12, 13)
        c7, c8, c9, c10, c11, c12, c13 = np.loadtxt(str(galaxy_name)+"/"+str(fileName), usecols=columns2, unpack=True)
        data = np.column_stack([x, y, z, v_x, v_y, v_z, mass, c7, c8, c9, c10, c11, c12, c13])

        # Sauvegarde des donnees
        datafile_path = str(galaxy_name) + "/data_centered/" + str(fileName)
        np.savetxt(datafile_path, data, fmt='%13.5E'*7 + '%10d' + '%13.5E'*6)
