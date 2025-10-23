# AnyVenue - Platform Booking Lapangan Olahraga Digital

## Nama-nama Anggota Kelompok
- Alya Nabilla Khamil (2406358094)
- Fakhri Husaini Romza (2406436972)
- Keisha Vania Laurent (2406437331)
- Naufal Fadli Rabbani (2406350785)
- Sahila Khairatul Athia (2406495716)

## Deskripsi Aplikasi
Platform website "AnyVenue" dirancang untuk memudahkan pengguna dalam mencari dan memesan *venue* olahraga. Fokus pada kemudahan pencarian, informasi ketersediaan slot waktu, dan proses reservasi *venue*. Pengguna dapat memasukkan lokasi, memilih *venue* sesuai jenis olahraga, melihat detail *venue*, dan melakukan *booking*.

### Kebermanfaatan
- *Untuk User (Pencari Venue)*: Menyediakan pengalaman yang **praktis, informatif, dan efisien**. Pengguna dapat dengan mudah mencari *venue* berdasarkan suatu kategori dan mendapatkan kepastian *booking* slot di waktu yang mereka inginkan.
- *Untuk Venue Partner (Pemilik Venue)*: Menyediakan **platform promosi digital** yang luas, mengoptimalkan tingkat pemanfaatan *venue*, dan mempermudah **manajemen jadwal/booking** secara digital.

## Daftar Modul yang Akan Diimplementasikan
1. *Autentikasi (Login/Register/Logout)*:
   - Memungkinkan pengguna untuk membuat akun baru, melakukan *login*, serta *logout* dengan aman. Modul ini juga mengatur hak akses agar fitur tertentu hanya dapat diakses sesuai *role*.
   
2. *Landing Page*:
   - Landing page berfungsi sebagai halaman utama yang menampilkan gambaran umum dari seluruh fitur yang tersedia dalam aplikasi. Pada bagian awal halaman, terdapat section perkenalan yang menjelaskan secara singkat tujuan dan konsep utama dari website ini. Setelah itu, pengguna dapat menemukan beberapa section overview yang menampilkan ringkasan dari fitur-fitur utama aplikasi, antara lain:
      - *Booking Venue/ Tambah Venue (untuk Owner):* menampilkan deskripsi singkat tentang fitur booking venue bagi pengguna atau dapat menambahkan venue baru bagi role owner.
      - *Event :* menampilkan ringkasan fitur untuk melihat daftar event yang sedang berlangsung bagi pengguna atau menambahkan event baru bagi owner.
      - *Review Lapangan:* menampilkan cuplikan fitur bagi pengguna untuk memberikan ulasan terhadap lapangan yang telah digunakan.

      Setiap section dilengkapi dengan tombol navigasi yang akan mengarahkan pengguna langsung ke halaman fitur terkait, sehingga landing page berfungsi sebagai pusat orientasi sekaligus pintu masuk ke seluruh modul utama dalam aplikasi.

3. *Venue* (Keisha Vania Laurent):
   - Menampilkan detail *venue* seperti deskripsi, lokasi, harga, kategori, dan review atau ulasan yang diberikan oleh pengguna. Modul ini juga menyediakan navigasi ke modul `Booking` dan `Review`.

4. *Booking* (Fakhri Husaini Romza):
   - Menampilkan halaman untuk melakukan *booking* kepada venue yang dipilih. Memiliki `User` yang bisa melakukan *booking* sebuah `Venue`, field `created_at` untuk tanggal *booking*.

5. *User* (Alya Nabilla Khamil):
   - Berfungsi untuk mengelola data dan aktivitas pengguna dalam sistem, yang terdiri dari dua jenis peran utama, yaitu `User` (pengguna biasa) dan `Owner` (pemilik venue). Halaman profil pengguna yang menampilkan informasi aktivitas masing-masing peran. Integrasi dengan modul `Venue` dan `Event` untuk menampilkan data terkait. Berikut detail halaman profil sesuai *role*:
        - User (Pengguna Biasa): Dapat melihat daftar *venue* yang sudah di-*booking*, dapat melihat *event* atau kompetisi yang diikuti, dapat melihat serta mengelola *review* yang telah dibuat terhadap venue.
        - Owner (Pemilik Venue): Memiliki kemampuan untuk melakukan CRUD (*Create, Read, Update, Delete*) terhadap data *venue*. Relasi bersifat *one-to-many*, di mana satu *owner* dapat memiliki lebih dari satu *venue*, dapat melakukan CRUD terhadap *event* yang diselenggarakan. Relasi juga bersifat *one-to-many*, di mana satu *owner* dapat membuat beberapa *event*.

6. *Review* (Sahila Khairatul Athia):
   - Memungkinkan `User` untuk memberikan `Review` terhadap suatu `Venue`. User dapat mengisi form *review* untuk *venue* tertentu dengan komentar/ulasan serta *rating* (1-5 bintang). *Review* yang dikirimkan akan ditampilkan di halaman detail *venue*, bersamaan dengan *review* dari *user* lainnya.
     
7. *Event* (Naufal Fadli Rabbani):
   -  Modul `Event` merupakan suatu fitur dimana `Owner` dapat menyelengarakan event dan membuka pendaftaran bagi `User` yang mau berpartisipasi. `User` dapat melakukan pendaftaran pada event yang diselenggrakan oleh `Owner`.

## Sumber Initial Dataset
List initial dataset -> [AnyVenue's Dataset](https://docs.google.com/spreadsheets/d/1-ULBMiPrgKrf5jqux1t8zMe6mDMGfZHzvRUlN7DwcL8/edit?usp=sharing)

Sumber Dataset -> [AYO - Super Sport Community App](https://ayo.co.id/venues)

## Role Pengguna
1. *User (Penyewa Venue)*:
    - Melihat daftar *venue* & melakukan *booking*
    - Melihat daftar *event* & mengikuti *event*
    - Memberikan *rating* dan *review*
    - Mengelola profil pribadi

2. *Owner (Pemilik Venue)*:
    - Menambahkan dan mengelola data *venue*
    - Menambahkan *event*
    - Melihat daftar *booking* pada *venue*-nya

## Tautan untuk menuju AnyVenue
[https://keisha-vania-anyvenue.pbp.cs.ui.ac.id/](https://keisha-vania-anyvenue.pbp.cs.ui.ac.id/)
## Prototype AnyVenue
[https://www.figma.com/design/hP4cysHH7mBI8mqyb1ZbYY/AnyVenue?node-id=24-1886&m=dev]
