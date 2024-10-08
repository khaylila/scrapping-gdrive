from bs4 import BeautifulSoup
import requests
import json

# {"nama":"SD NEGERI GADING I 177","sekolah_id":"C02EF67B-8D18-E111-BC52-4B6C161D5FDD","npsn":20532914,"jumlah_kirim":18,"ptk":25,"pegawai":8,"pd":597,"rombel":20,"jml_rk":10,"jml_lab":3,"jml_perpus":1,"induk_kecamatan":"Kec. Tambaksari","kode_wilayah_induk_kecamatan":"056020 ","induk_kabupaten":"Kota Surabaya","kode_wilayah_induk_kabupaten":"056000 ","induk_provinsi":"Prov. Jawa Timur","kode_wilayah_induk_provinsi":"050000 ","bentuk_pendidikan":"SD","status_sekolah":"Negeri","sinkron_terakhir":"25 Sep 2024 11:44:05","sekolah_id_enkrip":"E39CEEF0F710444E3432 "}
listAllSchool = []
allSurabaya = requests.get("https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=056000&semester_id=20241").text
allSurabaya = json.loads(allSurabaya)
for kecSekolah in allSurabaya:
    kodeWilayah = kecSekolah["kode_wilayah"].strip()
    sekolahWilayah = requests.get(f"https://dapo.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah={kodeWilayah}&semester_id=20241&bentuk_pendidikan_id=sd").text
    sekolahWilayah = json.loads(sekolahWilayah)
    for sekolah in sekolahWilayah:
        hashSekolah = sekolah["sekolah_id_enkrip"].strip()
        html_result = requests.get(f"https://dapo.kemdikbud.go.id/sekolah/{hashSekolah}").text
        # print(html_result)
        soup = BeautifulSoup(html_result, "lxml")
        # data sekolah
        dataSekolah = {}
        # nama sekolah
        schoolName = soup.find("h2")
        dataSekolah["nama_sekolah"] = schoolName.text

        # 
        profile = soup.find("div", class_="profile-usermenu").find_all("strong")
        dataSekolah["kepala_sekolah"] = profile[0].text
        dataSekolah["operator"] = profile[1].text
        dataSekolah["akreditasi"] = profile[2].text
        dataSekolah["kurikulum"] = profile[3].text
        dataSekolah["waktu"] = profile[4].text

        # 
        panelInfo = soup.find_all("div",class_="panel panel-info")

        # identitas sekolah
        identitasSekolah = panelInfo[0].find_all("p")
        dataSekolah["npsn"] = identitasSekolah[0].text.split(":")[-1].strip()
        dataSekolah["status"] = identitasSekolah[1].text.split(":")[-1].strip()
        dataSekolah["bentuk_pendidikan"] = identitasSekolah[2].text.split(":")[-1].strip()
        dataSekolah["status_kepemilikan"] = identitasSekolah[3].text.split(":")[-1].strip()
        dataSekolah["sk_pendirian"] = identitasSekolah[4].text.split(":")[-1].strip()
        dataSekolah["tanggal_sk_pendirian"] = identitasSekolah[5].text.split(":")[-1].strip()
        dataSekolah["sk_izin_operasional"] = identitasSekolah[6].text.split(":")[-1].strip()
        dataSekolah["tanggal_sk_izin_operasional"] = identitasSekolah[7].text.split(":")[-1].strip()

        # data pelengkap
        dataPelengkap = panelInfo[1].find_all("p")
        dataSekolah["kebutuhan_khusus"] = dataPelengkap[0].text.split(":")[-1].strip()
        dataSekolah["nama_bank"] = dataPelengkap[1].text.split(":")[-1].strip()
        dataSekolah["cabang_kcp"] = dataPelengkap[2].text.split(":")[-1].strip()
        dataSekolah["rekening_an"] = dataPelengkap[3].text.split(":")[-1].strip()

        # data rinci
        dataRinci = panelInfo[2].find_all("p")
        dataSekolah["status_bos"] = dataRinci[0].text.split(":")[-1].strip()
        dataSekolah["sertifikasi_iso"] = dataRinci[2].text.split(":")[-1].strip()
        dataSekolah["sumber_listrik"] = dataRinci[3].text.split(":")[-1].strip()
        dataSekolah["daya_listrik"] = dataRinci[4].text.split(":")[-1].strip()
        dataSekolah["kecepatan_internet"] = dataRinci[5].text.split(":")[-1].strip()

        #rekapitulasi
        rekapitulasi = requests.get(f'https://dapo.kemdikbud.go.id/rekap/sekolahDetail?semester_id=20241&sekolah_id={hashSekolah}').text
        print(rekapitulasi)
        # print(json.load(rekapitulasi))
        rekapitulasi = json.loads(rekapitulasi)[0]
        dataSekolah = dataSekolah | rekapitulasi

        # kontak
        kontak = panelInfo[7].find_all("p")
        dataSekolah["alamat"] = kontak[0].text.split(":")[-1].strip()
        dataSekolah["rt_rw"] = kontak[1].text.split(":")[-1].strip()
        dataSekolah["dusun"] = kontak[2].text.split(":")[-1].strip()
        dataSekolah["desa_kelurahan"] = kontak[3].text.split(":")[-1].strip()
        dataSekolah["kecamatan"] = kontak[4].text.split(":")[-1].strip()
        dataSekolah["kabupaten"] = kontak[5].text.split(":")[-1].strip()
        dataSekolah["provinsi"] = kontak[6].text.split(":")[-1].strip()
        dataSekolah["kodepos"] = kontak[7].text.split(":")[-1].strip()
        dataSekolah["lintang"] = kontak[8].text.split(":")[-1].strip()
        dataSekolah["bujur"] = kontak[9].text.split(":")[-1].strip()

        listAllSchool.append(dataSekolah)

print(len(listAllSchool))

with open('listSekolah.json', 'w', encoding='utf-8') as f:
    json.dump(listAllSchool, f, ensure_ascii=False, indent=4)
