import time
import random
def main():
    # --- game variable ---
    suhu_awal = 14.0  
    suhu_maks = 16.0  
    skor_kesadaran = 0
    hari = 1
    # --- ujian ---
    skenario_pool = [
        {
            "hari_nama": "SENIN: Ujian Konservasi Air 🚰",
            "tanya": "Kamu sedang menyikat gigi di pagi hari. Apa yang kamu lakukan dengan kran air?",
            "opsi": {
                "A": "Mematikan kran air saat menyikat gigi dan menyalakannya hanya saat berkumur.",
                "B": "Membiarkan kran tetap mengalir sepanjang menyikat gigi."
            },
            "pilihan_benar": "A",
            "efek_A": {"suhu": 0.0, "skor": 20},
            "efek_B": {"suhu": 0.4, "skor": 0},
            "fakta": "Fakta BMKG: Perubahan iklim merusak siklus air dan memicu krisis air bersih. Menghemat air sangat penting untuk menjaga cadangan air bumi!"
        },
        {
            "hari_nama": "SELASA: Ujian Transportasi Bersih 🚲",
            "tanya": "Kamu ingin pergi ke minimarket yang jaraknya cukup dekat (sekitar 500 meter).",
            "opsi": {
                "A": "Meminta diantar menggunakan sepeda motor.",
                "B": "Berjalan kaki atau bersepeda ke minimarket."
            },
            "pilihan_benar": "B",
            "efek_A": {"suhu": 0.5, "skor": 0},
            "efek_B": {"suhu": -0.1, "skor": 20},
            "fakta": "Fakta BMKG: Emisi gas rumah kaca dari pembakaran bahan bakar fosil kendaraan adalah pemicu utama bumi semakin mendidih (global boiling)."
        },
        {
            "hari_nama": "RABU: Ujian Manajemen Limbah ♻️",
            "tanya": "Di sekolah, kamu membeli minuman dingin dan diberi sedotan serta kantong plastik sekali pakai.",
            "opsi": {
                "A": "Menerimanya karena praktis dan langsung membuangnya ke tempat sampah nanti.",
                "B": "Menolak plastik dan menggunakan tumbler atau tas kain yang kamu bawa sendiri."
            },
            "pilihan_benar": "B",
            "efek_A": {"suhu": 0.3, "skor": 0},
            "efek_B": {"suhu": 0.0, "skor": 20},
            "fakta": "Fakta BMKG: Produksi plastik menghasilkan emisi karbon yang besar. Sampah plastik yang tertimbun juga merusak ekosistem lingkungan."
        },
        {
            "hari_nama": "KAMIS: Ujian Efisiensi Energi ⚡",
            "tanya": "Kamar tidurmu terasa agak hangat, padahal udara di luar rumah sedang sejuk.",
            "opsi": {
                "A": "Membuka jendela untuk membiarkan angin segar masuk terlebih dahulu.",
                "B": "Langsung menyalakan AC ke suhu paling dingin (16°C) sepanjang hari."
            },
            "pilihan_benar": "A",
            "efek_A": {"suhu": -0.1, "skor": 20},
            "efek_B": {"suhu": 0.4, "skor": 0},
            "fakta": "Fakta BMKG: Penggunaan energi listrik berlebih meningkatkan beban pembangkit listrik berbahan bakar batubara, menambah polusi udara."
        },
        {
            "hari_nama": "JUMAT: Ujian Akhir Komprehensif (Final Exam) 📝",
            "tanya": "Sekolahmu mengadakan program menanam pohon bersama di area gundul sekitar kota. Tindakanmu?",
            "opsi": {
                "A": "Ikut serta menanam pohon karena tahu pohon menyerap karbon dioksida di atmosfer.",
                "B": "Izin pulang cepat karena menganggap menanam satu pohon tidak akan mengubah suhu bumi."
            },
            "pilihan_benar": "A",
            "efek_A": {"suhu": -0.2, "skor": 20},
            "efek_B": {"suhu": 0.5, "skor": 0},
            "fakta": "Fakta BMKG: Reboisasi dan menjaga kelestarian pohon adalah salah satu langkah mitigasi paling efektif untuk menyerap emisi gas rumah kaca."
        }
    ]
    print("====================================================")
    print("🌍   WELCOME TO ECO-QUEST: EXAM WEEK EDITION!   🌍")
    print("====================================================")
    print("Misi kamu: Selesaikan ujian 5 hari berturut-turut.")
    print(f"Peringatan: Jangan sampai bumi mendidih melampaui {suhu_maks}°C!")
    print("====================================================\n")
    time.sleep(1.5)
    while hari <= 5 and suhu_awal < suhu_maks:
        skenario = skenario_pool[hari - 1]
        print(f"\n📝 === {skenario['hari_nama']} ===")
        print(f"🌡️ Suhu Bumi Saat Ini: {suhu_awal:.1f}°C / Batas Maks: {suhu_maks}°C")
        print(f"🏆 Total Nilai Ujian: {skor_kesadaran} Poin")
        print("----------------------------------------------------")
        print(skenario["tanya"])
        for kode, teks in skenario["opsi"].items():
            print(f"  [{kode}] {teks}")
        tebakan = input("\nMasukkan jawaban ujian kamu (A/B): ").upper().strip()
        while tebakan not in ["A", "B"]:
            tebakan = input("Pilihan tidak valid. Ketik A atau B: ").upper().strip()
        print("\n-----------------------------------------")
        if tebakan == skenario["pilihan_benar"]:
            print("🎉 JAWABAN BENAR! Nilai ujian kamu sempurna di subjek ini.")
            if tebakan == "A":
                suhu_awal += skenario["efek_A"]["suhu"]
                skor_kesadaran += skenario["efek_A"]["skor"]
            else:
                suhu_awal += skenario["efek_B"]["suhu"]
                skor_kesadaran += skenario["efek_B"]["skor"]
        else:
            print("❌ JAWABAN SALAH! Dampak buruk merusak nilai dan lingkungan kamu.")
            if tebakan == "A":
                suhu_awal += skenario["efek_A"]["suhu"]
                skor_kesadaran += skenario["efek_A"]["skor"]
            else:
                suhu_awal += skenario["efek_B"]["suhu"]
                skor_kesadaran += skenario["efek_B"]["skor"]
        print(f"\n💡 {skenario['fakta']}")
        print("-----------------------------------------")
        hari += 1
        time.sleep(2)
    # --- akhir exam dan endingnya ---
    print("\n====================================================")
    if suhu_awal >= suhu_maks:
        print(f"💀 KELUAR DARI KELAS! Suhu bumi mencapai {suhu_awal:.1f}°C sebelum ujian selesai.")
        print("Bumi mengalami Global Boiling. Rapor Akhir Kamu: F (Gagal) 🌋")
    else:
        print("🏆 CONGRATULATIONS! Kamu berhasil menyelesaikan Exam Week!")
        print(f"🌍 Kamu menjaga kestabilan iklim di suhu {suhu_awal:.1f}°C.")
        print(f"📊 Skor Akumulasi Ujian: {skor_kesadaran} Poin")
        # skor kamu
        if skor_kesadaran == 100:
            print("🎖️ Grade Rapor Anda: A+ (Pejuang Iklim Sejati!)")
        elif skor_kesadaran >= 80:
            print("🎖️ Grade Rapor Anda: A (Sangat Peduli Lingkungan)")
        elif skor_kesadaran >= 60:
            print("🎖️ Grade Rapor Anda: B (Cukup Baik, Pertahankan)")
        elif skor_kesadaran >= 40:
            print("🎖️ Grade Rapor Anda: C (Lulus, tapi butuh banyak belajar)")
        else:
            print("🎖️ Grade Rapor Anda: D (Hampir Gagal, ayo lebih peduli lingkungan!)")
            
    print("====================================================")

if __name__ == "__main__":
    main()
