import discord
from discord.ext import commands
import asyncio

# Kita mengaktifkan intents agar bot bisa membaca pesan teks di server
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

skenario_pool = [
    {
        "hari_nama": "SENIN: Ujian Konservasi Air 🚰",
        "tanya": "Kamu sedang menyikat gigi di pagi hari. Apa yang kamu lakukan dengan kran air?",
        "opsi": "A. Mematikan kran air saat menyikat gigi.\nB. Membiarkan kran tetap mengalir.",
        "pilihan_benar": "A",
        "efek": {"A": {"suhu": 0.0, "skor": 20}, "B": {"suhu": 0.4, "skor": 0}},
        "fakta": "Fakta BMKG: Perubahan iklim merusak siklus air dan memicu krisis air bersih. Menghemat air sangat penting!"
    },
    {
        "hari_nama": "SELASA: Ujian Transportasi Bersih 🚲",
        "tanya": "Kamu ingin pergi ke minimarket yang jaraknya cukup dekat (sekitar 500 meter).",
        "opsi": "A. Meminta diantar menggunakan sepeda motor.\nB. Berjalan kaki atau bersepeda.",
        "pilihan_benar": "B",
        "efek": {"A": {"suhu": 0.5, "skor": 0}, "B": {"suhu": -0.1, "skor": 20}},
        "fakta": "Fakta BMKG: Emisi gas rumah kaca dari bahan bakar fosil kendaraan memicu bumi mendidih (global boiling)."
    },
    {
        "hari_nama": "RABU: Ujian Manajemen Limbah ♻️",
        "tanya": "Di sekolah, kamu membeli minuman dingin dan diberi sedotan serta kantong plastik sekali pakai.",
        "opsi": "A. Menerimanya karena praktis.\nB. Menolak plastik dan menggunakan tumbler sendiri.",
        "pilihan_benar": "B",
        "efek": {"A": {"suhu": 0.3, "skor": 0}, "B": {"suhu": 0.0, "skor": 20}},
        "fakta": "Fakta BMKG: Produksi plastik menghasilkan emisi karbon besar yang mengotori bumi."
    },
    {
        "hari_nama": "KAMIS: Ujian Efisiensi Energi ⚡",
        "tanya": "Kamar tidurmu terasa agak hangat, padahal udara di luar rumah sedang sejuk.",
        "opsi": "A. Membuka jendela untuk membiarkan angin masuk.\nB. Langsung menyalakan AC ke suhu paling dingin (16°C).",
        "pilihan_benar": "A",
        "efek": {"A": {"suhu": -0.1, "skor": 20}, "B": {"suhu": 0.4, "skor": 0}},
        "fakta": "Fakta BMKG: Pemborosan listrik meningkatkan beban pembangkit listrik batubara, menambah polusi udara."
    },
    {
        "hari_nama": "JUMAT: Ujian Akhir Komprehensif (Final Exam) 📝",
        "tanya": "Sekolahmu mengadakan program menanam pohon bersama di area gundul sekitar kota. Tindakanmu?",
        "opsi": "A. Ikut serta menanam pohon.\nB. Izin pulang cepat.",
        "pilihan_benar": "A",
        "efek": {"A": {"suhu": -0.2, "skor": 20}, "B": {"suhu": 0.5, "skor": 0}},
        "fakta": "Fakta BMKG: Menanam pohon (reboisasi) sangat efektif untuk menyerap emisi gas rumah kaca di atmosfer."
    }
]

@bot.event
async def on_ready():
    print(f"🤖 Bot Berhasil Online! Masuk sebagai: {bot.user.name}")

# --- BOT GAME COMMAND ---
@bot.command()
async def mulai_ujian(ctx):
    suhu_awal = 14.0
    suhu_maks = 16.0
    skor_kesadaran = 0
    
    await ctx.send("====================================================\n"
                   "🌍   **WELCOME TO ECO-QUEST: EXAM WEEK EDITION!** 🌍\n"
                   "====================================================\n"
                   "Misi kamu: Selesaikan ujian 5 hari berturut-turut lewat chat ini.\n"
                   f"Peringatan: Jangan sampai bumi mendidih melampaui {suhu_maks}°C!\n"
                   "Ketik jawaban kamu dengan membalas **A** atau **B** langsung.")
    
    await asyncio.sleep(2)

    for hari in range(1, 6):
        if suhu_awal >= suhu_maks:
            break
            
        skenario = skenario_pool[hari - 1]
        
        # Kirim status hari dan pertanyaan ke channel Discord
        status_msg = (f"\n📝 === **{skenario['hari_nama']}** ===\n"
                      f"🌡️ Suhu Bumi: `{suhu_awal:.1f}°C` / Batas: `{suhu_maks}°C`\n"
                      f"🏆 Total Nilai: `{skor_kesadaran} Poin`\n"
                      f"**Pertanyaan:** {skenario['tanya']}\n"
                      f"{skenario['opsi']}")
        await ctx.send(status_msg)

        # Fungsi check untuk memastikan bot hanya menerima jawaban dari orang yang mengetik !mulai_ujian
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in ["A", "B"]

        try:
            # Menunggu jawaban user selama 60 detik
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            jawaban = msg.content.upper().strip()
        except asyncio.TimeoutError:
            await ctx.send("⏰ Waktu habis! Kamu dianggap tidak menjawab ujian hari ini.")
            jawaban = "SALAH"  # Jika timeout, otomatis tidak dapat poin

        # Hitung dampak pilihan
        if jawaban == skenario["pilihan_benar"]:
            await ctx.send("🎉 **JAWABAN BENAR!** Nilai ujian kamu sempurna di subjek ini.")
            suhu_awal += skenario["efek"][jawaban]["suhu"]
            skor_kesadaran += skenario["efek"][jawaban]["skor"]
        else:
            await ctx.send("❌ **JAWABAN SALAH!** Dampak buruk merusak nilai dan lingkungan kamu.")
            # Ambil efek sebaliknya atau efek jawaban salah
            efek_salah = "B" if skenario["pilihan_benar"] == "A" else "A"
            # Jika user menjawab salah (bukan timeout) gunakan efek input mereka, jika timeout pakai efek buruk default
            pilihan_efek = jawaban if jawaban in ["A", "B"] else efek_salah
            suhu_awal += skenario["efek"][pilihan_efek]["suhu"]
            skor_kesadaran += skenario["efek"][pilihan_efek]["skor"]

        # Tampilkan fakta edukatif BMKG
        await ctx.send(f"💡 *{skenario['fakta']}*\n-----------------------------------------")
        await asyncio.sleep(2)

    # --- ENDING RAPOR AKHIR ---
    await ctx.send("\n====================================================")
    if suhu_awal >= suhu_maks:
        await ctx.send(f"💀 **GAME OVER!** Suhu bumi mencapai `{suhu_awal:.1f}°C` sebelum ujian selesai.\n"
                       "Bumi mengalami Global Boiling. Rapor Akhir Kamu: **F (Gagal)** 🌋")
    else:
        # Menentukan grade nilai
        if skor_kesadaran == 100: grade = "A+ (Pejuang Iklim Sejati!)"
        elif skor_kesadaran >= 80: grade = "A (Sangat Peduli Lingkungan)"
        elif skor_kesadaran >= 60: grade = "B (Cukup Baik, Pertahankan)"
        elif skor_kesadaran >= 40: grade = "C (Lulus, tapi butuh banyak belajar)"
        else: grade = "D (Hampir Gagal!)"
            
        await ctx.send("🏆 **CONGRATULATIONS!** Kamu berhasil menyelesaikan Exam Week!\n"
                       f"🌍 Kamu menjaga kestabilan iklim di suhu `{suhu_awal:.1f}°C`.\n"
                       f"📊 Skor Akumulasi Ujian: `{skor_kesadaran} Poin`\n"
                       f"🎖️ **Grade Rapor Anda:** {grade}")
    await ctx.send("====================================================")

bot.run("token here")
