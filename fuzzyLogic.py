import pandas as pd
import numpy as np
import skfuzzy as fuzz

df = pd.read_excel('data_buah.xlsx')

def proses_fuzzy(daftar_buah):

    # RENTANG SEMESTA
    karbohidrat = np.arange(0, 30.1, 0.1)
    serat = np.arange(0, 10.1, 0.1)
    x_kelayakan = np.arange(0, 1.1, 0.1)

    # FUZZY INPUT KARBOHIDRAT
    karbo_r = fuzz.trapmf(karbohidrat, [0, 0, 11, 12])
    karbo_s = fuzz.trimf(karbohidrat, [11, 16, 21])
    karbo_t = fuzz.trapmf(karbohidrat, [20, 21, 30, 30])

    # FUZZY INPUT SERAT
    serat_r = fuzz.trapmf(serat, [0, 0, 3, 4])
    serat_s = fuzz.trimf(serat, [3, 5, 7])
    serat_t = fuzz.trapmf(serat, [6, 7, 10, 10])

    # FUZZY OUTPUT
    kelayakan_ca = fuzz.trimf(x_kelayakan, [0, 0, 0.5])
    kelayakan_a = fuzz.trimf(x_kelayakan, [0.5, 1, 1])

    hasil_buah = []

    # LOOP BUAH
    for buah in daftar_buah:

        data = df[df['Nama Buah'].str.lower() == buah.lower()]

        if data.empty:
            continue

        karbo_input = float(data['Karbohidrat (g)'].values[0])
        serat_input = float(data['Serat (g)'].values[0])

        # FUZZIFIKASI
        karbo_r_val = fuzz.interp_membership(karbohidrat, karbo_r, karbo_input)
        karbo_s_val = fuzz.interp_membership(karbohidrat, karbo_s, karbo_input)
        karbo_t_val = fuzz.interp_membership(karbohidrat, karbo_t, karbo_input)

        serat_r_val = fuzz.interp_membership(serat, serat_r, serat_input)
        serat_s_val = fuzz.interp_membership(serat, serat_s, serat_input)
        serat_t_val = fuzz.interp_membership(serat, serat_t, serat_input)

        # RULE
        a1 = np.fmin(karbo_r_val, serat_t_val)
        r1 = np.fmin(a1, kelayakan_a)

        a2 = np.fmin(karbo_r_val, serat_s_val)
        r2 = np.fmin(a2, kelayakan_a)

        a3 = np.fmin(karbo_r_val, serat_r_val)
        r3 = np.fmin(a3, kelayakan_ca)

        a4 = np.fmin(karbo_s_val, serat_t_val)
        r4 = np.fmin(a4, kelayakan_a)

        a5 = np.fmin(karbo_s_val, serat_s_val)
        r5 = np.fmin(a5, kelayakan_a)

        a6 = np.fmin(karbo_s_val, serat_r_val)
        r6 = np.fmin(a6, kelayakan_ca)

        a7 = np.fmin(karbo_t_val, serat_t_val)
        r7 = np.fmin(a7, kelayakan_ca)

        a8 = np.fmin(karbo_t_val, serat_s_val)
        r8 = np.fmin(a8, kelayakan_ca)

        a9 = np.fmin(karbo_t_val, serat_r_val)
        r9 = np.fmin(a9, kelayakan_ca)

        # AGREGASI
        aggregated = np.fmax.reduce([r1, r2, r3, r4, r5, r6, r7, r8, r9])

        # DEFUZZIFIKASI
        kelayakan = np.sum(x_kelayakan * aggregated) / np.sum(aggregated)

        kategori = "Aman" if kelayakan > 0.5 else "Cukup Aman"

        hasil_buah.append({
            'buah': buah,
            'karbohidrat': karbo_input,
            'serat': serat_input,
            'kelayakan': kelayakan,
            'kategori': kategori
        })

    # TOTAL
    total_kelayakan = sum(item['kelayakan'] for item in hasil_buah)

    rata_kelayakan = total_kelayakan / len(hasil_buah)

    status_kombinasi = "AMAN" if rata_kelayakan > 0.5 else "CUKUP AMAN"

    # TOTAL KONSUMSI
    if rata_kelayakan <= 0.5:
        total_konsumsi = 100 + (rata_kelayakan / 0.5) * 100
    else:
        total_konsumsi = 200 + ((rata_kelayakan - 0.5) / 0.5) * 100

    # REKOMENDASI PER BUAH
    for item in hasil_buah:

        proporsi = item['kelayakan'] / total_kelayakan
        gram = proporsi * total_konsumsi

        item['rekomendasi'] = round(gram, 1)

    return hasil_buah, rata_kelayakan, status_kombinasi, total_konsumsi

if __name__ == "__main__":

    daftar_buah = ["Jambu Biji", "Buah Naga"]

    hasil_buah, rata_kelayakan, status_kombinasi, total_konsumsi = proses_fuzzy(daftar_buah)

    print("Status Kombinasi:", status_kombinasi)
    print("Rata-rata Kelayakan:", rata_kelayakan)
    print("Total Konsumsi:", total_konsumsi)

    for item in hasil_buah:
        print(item)