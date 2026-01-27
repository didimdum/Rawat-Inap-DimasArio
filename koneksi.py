from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from fpdf import FPDF
from datetime import datetime, time
import mysql.connector
from io import BytesIO


app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rawatinap_dimas'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn 

def id_otomatis(prefix, nama_tabel, kolom_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT {kolom_id} FROM {nama_tabel} WHERE {kolom_id} LIKE %s ORDER BY {kolom_id} DESC LIMIT 1", (prefix + '%',))
        hasil = cursor.fetchone()
        cursor.close()
        conn.close()
        if hasil and kolom_id in hasil:
            id_terakhir = hasil[kolom_id]
            no = int(id_terakhir.replace(prefix, '')) + 1
        else:
            no = 1
        id_baru = f"{prefix}{str(no).zfill(3)}"
        return id_baru
    except Exception as e:
        print(f"Error generating ID: {e}")
        return None
#
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT t.*, p.nama AS nama_pasien, r.tgl_masuk, r.tgl_keluar FROM tarnsaksi_dimas t LEFT JOIN pasien_dimas p ON t.id_pasien = p.id_pasien LEFT JOIN rawat_inap_dimas r ON t.id_rawat = r.id_rawat ORDER BY t.tanggal_transaksi ASC")
        transaksi = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', transaksi=transaksi)
    except Exception as e:
        return f"Koneksi gagal ke database: {e}"

@app.route('/index-pasien')
def index_pasien():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_dimas ORDER BY id_pasien ASC")
        pasien = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index-pasien.html', pasien=pasien)
    except Exception as e:
        return f"Koneksi gagal ke database: {e}"

@app.route('/form-pasien', methods=['GET', 'POST'])
def form_pasien():
    if request.method == 'POST':
        DimasIDPasien = request.form['DimasIDPasien']
        DimasNama = request.form['DimasNama']
        DimasAlamat = request.form['DimasAlamat']
        DimasKontak = request.form['DimasKontak']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO pasien_dimas (id_pasien, nama, alamat, kontak) VALUES (%s, %s, %s, %s)"
            val = (DimasIDPasien, DimasNama, DimasAlamat, DimasKontak)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/index-pasien')
        except Exception as e:
            return f"Gagal menyimpan data ke database: {e}"
    else:
        id_otomatis_pasien = id_otomatis('P-', 'pasien_dimas', 'id_pasien')
        return render_template('form-pasien.html', id_otomatis_pasien=id_otomatis_pasien)

@app.route('/input', methods=['GET', 'POST'])
def input_transaksi():
    try:
        if request.method == 'POST':
            conn = get_db_connection()
            cursor = conn.cursor()
            DimasIDTransaksi = id_otomatis('T-', 'tarnsaksi_dimas', 'id_transaksi')
            if not DimasIDTransaksi:
                return "Gagal generate ID transaksi, silakan coba lagi."
            DimasIDPasien = request.form["DimasIDPasien"]
            DimasIDRawat = request.form['DimasIDRawat']
            DimasTotalBiaya = request.form.get("DimasTotalBiaya")
            DimasStatusPembayaran = request.form['DimasStatusPembayaran']
            DimasTanggalTransaksi = request.form['DimasTanggalTransaksi']

            try:
                tmpc = conn.cursor(dictionary=True)
                tmpc.execute("SELECT id_kamar, tgl_masuk, tgl_keluar FROM rawat_inap_dimas WHERE id_rawat=%s", (DimasIDRawat,))
                rawat = tmpc.fetchone()
                if rawat and rawat.get('id_kamar') and rawat.get('tgl_masuk') and rawat.get('tgl_keluar'):
                    id_kamar = rawat['id_kamar']
                    tgl_masuk = rawat['tgl_masuk']
                    tgl_keluar = rawat['tgl_keluar']
                    delta = (tgl_keluar - tgl_masuk).days
                    days = delta if delta>0 else 1
                    tmpc.execute("SELECT harga FROM kamar_dimas WHERE id_kamar=%s", (id_kamar,))
                    k = tmpc.fetchone()
                    if k and k.get('harga') is not None:
                        harga = k['harga']
                        DimasTotalBiaya = harga * days
                tmpc.close()
            except Exception:

                pass
            sql = "INSERT INTO tarnsaksi_dimas (id_transaksi, id_pasien, id_rawat, total_biaya, status_pembayaran, tanggal_transaksi) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (DimasIDTransaksi, DimasIDPasien, DimasIDRawat, DimasTotalBiaya, DimasStatusPembayaran, DimasTanggalTransaksi))
            conn.commit()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT t.*, p.nama AS nama_pasien FROM tarnsaksi_dimas t LEFT JOIN pasien_dimas p ON t.id_pasien = p.id_pasien ORDER BY t.tanggal_transaksi DESC")
            transaksi = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('index.html', transaksi=transaksi)
        else:
            return render_template('form.html')
    except Exception as e:
        return f"Koneksi gagal ke database: {e}"


#input dta transk
@app.route('/form-mapel', methods=['GET', 'POST'])
def form_mapel():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_pasien, nama FROM pasien_dimas ORDER BY nama")
    pasien_list = cursor.fetchall()
    cursor.execute("SELECT id_rawat, id_pasien FROM rawat_inap_dimas ORDER BY id_rawat")
    rawat_list = cursor.fetchall()
    # Generate ID otomatis
    id_otomatis_transaksi = id_otomatis('T-', 'tarnsaksi_dimas', 'id_transaksi')
    cursor.close()
    conn.close()
    return render_template('form-mapel.html', pasien_list=pasien_list, rawat_list=rawat_list, id_otomatis_transaksi=id_otomatis_transaksi)


@app.route('/edit-transaksi/<string:id>', methods=['GET', 'POST'])
def edit_transaksi(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        DimasIDPasien = request.form['DimasIDPasien']
        DimasIDRawat = request.form['DimasIDRawat']
        DimasTotalBiaya = request.form['DimasTotalBiaya']
        DimasStatusPembayaran = request.form['DimasStatusPembayaran']
        DimasTanggalTransaksi = request.form['DimasTanggalTransaksi']
        cursor = conn.cursor(dictionary=True)
        try:
            tmpc = conn.cursor(dictionary=True)
            tmpc.execute("SELECT id_kamar, tgl_masuk, tgl_keluar FROM rawat_inap_dimas WHERE id_rawat=%s", (DimasIDRawat,))
            rawat = tmpc.fetchone()
            if rawat and rawat.get('id_kamar') and rawat.get('tgl_masuk') and rawat.get('tgl_keluar'):
                id_kamar = rawat['id_kamar']
                delta = (rawat['tgl_keluar'] - rawat['tgl_masuk']).days
                days = delta if delta>0 else 1
                tmpc.execute("SELECT harga FROM kamar_dimas WHERE id_kamar=%s", (id_kamar,))
                k = tmpc.fetchone()
                if k and k.get('harga') is not None:
                    DimasTotalBiaya = k['harga'] * days
            tmpc.close()
        except Exception:
            pass

        sql = "UPDATE tarnsaksi_dimas SET id_pasien=%s, id_rawat=%s, total_biaya=%s, status_pembayaran=%s, tanggal_transaksi=%s WHERE id_transaksi=%s"
        cursor.execute(sql, (DimasIDPasien, DimasIDRawat, DimasTotalBiaya, DimasStatusPembayaran, DimasTanggalTransaksi, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        #pilih pasien
        cursor.execute("SELECT id_pasien, nama FROM pasien_dimas ORDER BY nama")
        pasien_list = cursor.fetchall()
        cursor.execute("SELECT id_rawat, id_pasien FROM rawat_inap_dimas ORDER BY id_rawat")
        rawat_list = cursor.fetchall()
        cursor.execute("SELECT * FROM tarnsaksi_dimas WHERE id_transaksi=%s", (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data is None:
            return "Transaksi tidak ditemukan"
        return render_template('edit-transaksi.html', data=data, pasien_list=pasien_list, rawat_list=rawat_list)



@app.route('/hapus-transaksi/<string:id>', methods=['POST'])
def hapus_transaksi(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarnsaksi_dimas WHERE id_transaksi=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Gagal menghapus transaksi: {e}"

@app.route('/cetak')
def cetak():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_pasien, nama, alamat, kontak FROM pasien_dimas ORDER BY id_pasien ASC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, txt="Laporan data Pasien", ln=1, align='C')
        pdf.ln(5)

        pdf.set_font("Arial", size=11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(40, 10, "ID Pasien", border=1, fill=True)
        pdf.cell(60, 10, "Nama", border=1, fill=True)
        pdf.cell(60, 10, "Alamat", border=1, fill=True)
        pdf.cell(30, 10, "Kontak", border=1, fill=True)
        pdf.ln()

        pdf.set_fill_color(255, 255, 255)
        for d in data:
            pdf.cell(40, 10, d['id_pasien'], 1, fill=True)
            pdf.cell(60, 10, d['nama'], 1, fill=True)
            pdf.cell(60, 10, d['alamat'], 1, fill=True)
            pdf.cell(30, 10, d['kontak'], 1, fill=True)
            pdf.ln()
        


            """response = make_response(pdf.output(dest='S').encode('latin1'))
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=laporan_pasien.pdf'

            return response
        except Exception as e:
            return f"Gagal mencetak laporan: {e}"""
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        
        return send_file(pdf_output, as_attachment=True, 
        download_name='laporan_pasien.pdf', 
        mimetype='application/pdf'
        )
    except Exception as e:
        return f"Gagal mencetak laporan: {e}"

if __name__ == '__main__':
    app.run(debug=True)