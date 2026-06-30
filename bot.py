import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- GLOBAL LEADERBOARD DICTIONARY ---
# Stores data like: { "Username": skor_tertinggi }
leaderboard = {}

skenario_pool = [
    {
        "hari_nama": "SENIN: Ujian Konservasi Air 🚰",
        "tanya": "Berdasarkan teks bacaan tadi, apa tindakan terbaik saat menyikat gigi di pagi hari?",
        "opsi": "A. Mematikan kran air saat menyikat gigi.\nB. Membiarkan kran tetap mengalir.",
        "pilihan_benar": "A",
        "efek": {"A": {"suhu": 0.0, "skor": 20}, "B": {"suhu": 0.4, "skor": 0}},
        "fakta": "Fakta BMKG: Menghemat air sangat penting untuk menjaga cadangan air bersih bumi!"
    },
    {
        "hari_nama": "SELASA: Ujian Transportasi Bersih 🚲",
        "tanya": "Jika jarak minimarket sangat dekat (500 meter), apa pilihan transportasi ramah lingkungan yang benar?",
        "opsi": "A. Meminta diantar menggunakan sepeda motor.\nB. Berjalan kaki atau bersepeda.",
        "pilihan_benar": "B",
        "efek": {"A": {"suhu": 0.5, "skor": 0}, "B": {"suhu": -0.1, "skor": 20}},
        "fakta": "Fakta BMKG: Emisi kendaraan fosil memicu bumi mendidih (global boiling)."
    },
    {
        "hari_nama": "RABU: Ujian Manajemen Limbah ♻️",
        "tanya": "Bagaimana cara mengurangi limbah plastik sekali pakai di lingkungan sekolah?",
        "opsi": "A. Menerima plastik karena praktis.\nB. Menolak plastik dan menggunakan tumbler sendiri.",
        "pilihan_benar": "B",
        "efek": {"A": {"suhu": 0.3, "skor": 0}, "B": {"suhu": 0.0, "skor": 20}},
        "fakta": "Fakta BMKG: Sampah plastik yang tertimbun lama merusak ekosistem lingkungan secara masif."
    },
    {
        "hari_nama": "KAMIS: Ujian Efisiensi Energi ⚡",
        "tanya": "Apa rekomendasi terbaik saat kamar tidur terasa agak hangat padahal udara luar sejuk?",
        "opsi": "A. Membuka jendela untuk angin segar.\nB. Menyala AC ke suhu paling dingin (16°C).",
        "pilihan_benar": "A",
        "efek": {"A": {"suhu": -0.1, "skor": 20}, "B": {"suhu": 0.4, "skor": 0}},
        "fakta": "Fakta BMKG: Penggunaan AC berlebih meningkatkan beban pembangkit listrik batubara."
    },
    {
        "hari_nama": "JUMAT: Ujian Akhir Komprehensif (Final Exam) 📝",
        "tanya": "Mengapa program menanam pohon bersama sangat krusial bagi masa depan atmosfer kita?",
        "opsi": "A. Ikut menanam pohon untuk menyerap karbon dioksida.\nB. Izin pulang cepat.",
        "pilihan_benar": "A",
        "efek": {"A": {"suhu": -0.2, "skor": 20}, "B": {"suhu": 0.5, "skor": 0}},
        "fakta": "Fakta BMKG: Reboisasi adalah langkah mitigasi terbaik menyerap emisi gas rumah kaca."
    }
]

@bot.event
async def on_ready():
    print(f"🤖 Bot Berhasil Online! Masuk sebagai: {bot.user.name}")

# --- COMMAND 1: COMMAND UTAMA UJIAN TRICK ---
@bot.command()
async def mulai_ujian(ctx):
    suhu_awal = 14.0
    suhu_maks = 16.0
    skor_kesadaran = 0
    
    await ctx.send("====================================================\n"
                   "🌍   **WELCOME TO ECO-QUEST: TRICK EXAM WEEK!** 🌍\n"
                   "====================================================\n"
                   "⚠️ **PERINGATAN SEBELUM UJIAN MULAI:**\n"
                   "Aku akan mengirimkan sebuah dokumen materi studi penting. Di dalamnya terdapat info penting, "
                   "cerita palsu, dan jawaban ujian tersembunyi. Kamu punya waktu **2 MENIT** untuk membaca "
                   "dan menghafalnya sebelum materi ini **DIHAPUS OTOMATIS** selamanya!\n"
                   "====================================================")
    
    await asyncio.sleep(5)

    # --- INDONESIAN INFORMATION OVERLOAD BLOCKS ---
    info_text = (
        "📚 **[MATERI STUDI UTAMA - BACA SEBELUM DIHAPUS!]** 📚\n\n"
        "**Paragraf 1 (Krisis Air):** Kemarin lusa, Budi pergi membeli es krim cokelat di dekat rumahnya, namun tokonya tutup. "
        "Berbicara tentang air, BMKG menegaskan krisis air bersih semakin nyata akibat siklus iklim yang rusak. Maka dari itu, "
        "saat menyikat gigi di pagi hari, tindakan esensial yang wajib dilakukan adalah mematikan kran air saat menyikat gigi "
        "dan menyalakannya hanya saat berkumur agar tidak membuang galon air sia-sia.\n\n"
        "**Paragraf 2 (Transportasi):** Kucing peliharaan milik kepala sekolah kemarin melompat ke atas atap dan tidak bisa turun selama dua jam. "
        "Di sisi lain, emisi karbon kendaraan bermotor mempercepat global boiling. Solusi terbaik jika kamu hanya ingin pergi ke minimarket "
        "yang berjarak sangat dekat sekitar 500 meter adalah berjalan kaki atau bersepeda, bukan menggunakan kendaraan bermotor.\n\n"
        "**Paragraf 3 (Manajemen Sampah):** Pada tahun 1998, sebuah riset mengatakan bahwa bermain game terlalu lama bisa membuat mata lelah. "
        "Namun yang merusak bumi kita hari ini adalah penumpukan plastik sekali pakai di TPA. Strategi utama mengurangi limbah plastik di sekolah "
        "adalah dengan tegas menolak plastik sekali pakai dan membawa tumbler atau tas kain sendiri dari rumah.\n\n"
        "**Paragraf 4 (Efisiensi Energi):** Memasak mie instan membutuhkan waktu sekitar 3 sampai 5 menit agar matang sempurna. "
        "Tapi tahukah kamu? Boros listrik memperparah polusi pembangkit batubara. Jika kamar tidur terasa agak hangat padahal udara luar sejuk, "
        "cara efisiensi terbaik adalah membuka jendela untuk membiarkan angin masuk , bukannya langsung menyalakan AC ke suhu 16°C sepanjang hari.\n\n"
        "**Paragraf 5 (Mitigasi Karbon):** Kemarin sore hujan turun sangat deras membuat jemuran milik bu RT basah kuyup kembali. "
        "Meskipun begitu, atmosfer bumi bisa diselamatkan lewat reboisasi. Mengikuti program menanam pohon bersama di area gundul "
        "sangat krusial karena pohon bertindak sebagai penyerap karbon dioksida paling efektif di bumi."
    )

    # Kirim info dump dan simpan pesannya ke variabel
    materi_msg = await ctx.send(info_text)
    
    # Hitung mundur 2 menit (120 detik)
    await ctx.send("⏱️ *Waktu membaca dimulai! Kamu punya waktu 60 detik sebelum pesan di atas menghilang...*")
    await asyncio.sleep(60.0)
    
    # Hapus materi studi secara paksa!
    await materi_msg.delete()
    await ctx.send("💥 **WAKTU HABIS! materi studi telah dihancurkan!** Sekarang, mari kita lihat seberapa baik ingatanmu. Ujian dimulai!")
    await asyncio.sleep(2)

    # --- MAIN GAME LOOP ---
    for hari in range(1, 6):
        if suhu_awal >= suhu_maks:
            break
            
        skenario = skenario_pool[hari - 1]
        
        status_msg = (f"\n📝 === **{skenario['hari_nama']}** ===\n"
                      f"🌡️ Suhu Bumi: `{suhu_awal:.1f}°C` / Batas: `{suhu_maks}°C`\n"
                      f"🏆 Total Nilai: `{skor_kesadaran} Poin`\n"
                      f"**Pertanyaan:** {skenario['tanya']}\n"
                      f"{skenario['opsi']}")
        await ctx.send(status_msg)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in ["A", "B"]

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0) # 30 detik per soal
            jawaban = msg.content.upper().strip()
        except asyncio.TimeoutError:
            await ctx.send("⏰ Waktu habis! Kamu ragu-ragu karena lupa ya?")
            jawaban = "SALAH"

        if jawaban == skenario["pilihan_benar"]:
            await ctx.send("🎉 **JAWABAN BENAR!** Ingatanmu tajam.")
            suhu_awal += skenario["efek"][jawaban]["suhu"]
            skor_kesadaran += skenario["efek"][jawaban]["skor"]
        else:
            await ctx.send("❌ **JAWABAN SALAH!** Kamu terjebak informasi palsu ya?")
            efek_salah = "B" if skenario["pilihan_benar"] == "A" else "A"
            pilihan_efek = jawaban if jawaban in ["A", "B"] else efek_salah
            suhu_awal += skenario["efek"][pilihan_efek]["suhu"]
            skor_kesadaran += skenario["efek"][pilihan_efek]["skor"]

        await ctx.send(f"💡 *{skenario['fakta']}*\n-----------------------------------------")
        await asyncio.sleep(2)

    # --- ENDING & LEADERBOARD SAVE ---
    player_name = ctx.author.name
    await ctx.send("\n====================================================")
    if suhu_awal >= suhu_maks:
        await ctx.send(f"💀 **GAME OVER!** Bumi mendidih pada suhu `{suhu_awal:.1f}°C`.\nRapor Akhir: **F (Gagal)** 🌋")
        final_skor = skor_kesadaran
    else:
        if skor_kesadaran == 100: grade = "A+ (Pejuang Iklim Sejati!)"
        elif skor_kesadaran >= 80: grade = "A"
        elif skor_kesadaran >= 60: grade = "B"
        else: grade = "C"
            
        await ctx.send("🏆 **HEBAT!** Kamu berhasil menyelesaikan Exam Week!\n"
                       f"📊 Skor Akhir: `{skor_kesadaran} Poin`\n"
                       f"🎖️ **Grade Rapor:** {grade}")
        final_skor = skor_kesadaran

    # Simpan skor tertinggi pemain ke Leaderboard global
    if player_name not in leaderboard or final_skor > leaderboard[player_name]:
        leaderboard[player_name] = final_skor
        await ctx.send(f"💾 Skor `{final_skor}` poin milik **{player_name}** berhasil dicatat ke sistem!")
    await ctx.send("====================================================")


# --- COMMAND 2: MELIHAT PAPAN PERINGKAT ---
@bot.command()
async def papan_skor(ctx):
    if not leaderboard:
        await ctx.send("📊 **Leaderboard Kosong!** Belum ada yang berani mengambil tantangan ujian ini.")
        return
        
    # Urutkan dari skor tertinggi ke terendah
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    
    leaderboard_text = "🏆 **PAPAN SKOR TERTINGGI: ECO-SCHOLARS** 🏆\n-----------------------------------------\n"
    for rank, (user, score) in enumerate(sorted_leaderboard, start=1):
        leaderboard_text += f"**{rank}.** {user} — `{score} Poin`\n"
    leaderboard_text += "-----------------------------------------"
    
    await ctx.send(leaderboard_text)

bot.run("token here")
