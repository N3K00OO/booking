import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
# Import model dari app venue
from venue.models import Venue, City, Category
# Import model Profile dari app user
from account.models import Profile  

class Command(BaseCommand):
    help = 'Mengimpor data venue dari file venues_data.csv, menghubungkan owner ke user.Profile'

    def handle(self, *args, **options):
        file_path = 'venues_data.csv'

        # 1. Dapatkan Profile superuser sebagai FALLBACK
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(self.style.ERROR('ERROR: Superuser tidak ditemukan. Harap buat superuser terlebih dahulu (python manage.py createsuperuser).'))
            return

        # Cari/buat Profile untuk superuser, pastikan role-nya OWNER
        fallback_owner_profile, created = Profile.objects.get_or_create(
            user=superuser,
            defaults={'role': 'OWNER'} # Set role OWNER jika baru dibuat
        )
        # Jika Profile sudah ada tapi role bukan OWNER, update
        if not created and fallback_owner_profile.role != 'OWNER':
            fallback_owner_profile.role = 'OWNER'
            fallback_owner_profile.save()
            self.stdout.write(self.style.WARNING(f"Role untuk Profile superuser '{superuser.username}' diubah menjadi OWNER."))

        self.stdout.write(self.style.SUCCESS(f'Memulai impor data dari {file_path}...'))
        self.stdout.write(f"Owner default (fallback) akan di-set ke Profile: {fallback_owner_profile.user.username} ({fallback_owner_profile.role})")

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Cek apakah header owner_username ada
                if 'owner_username' not in reader.fieldnames:
                     self.stdout.write(self.style.WARNING(
                        f'Kolom "owner_username" tidak ditemukan di {file_path}. Semua venue akan dimiliki oleh fallback owner.'
                    ))

                venues_created = 0
                venues_updated = 0
                users_created = set()
                profiles_created = set()
                roles_updated = set()

                for row in reader:

                    # 2. Logika Owner Baru (menggunakan Profile)
                    owner_username = row.get('owner_username') # Ambil username dari CSV

                    if owner_username:
                        # Cari/buat User
                        owner_user, user_created = User.objects.get_or_create(
                            username=owner_username,
                            defaults={'first_name': owner_username}
                        )
                        if user_created:
                            users_created.add(owner_username)

                        # Cari/buat Profile yang terhubung ke User
                        owner_profile, profile_created = Profile.objects.get_or_create(
                            user=owner_user,
                            defaults={'role': 'OWNER'} # Langsung set OWNER jika baru
                        )
                        if profile_created:
                           profiles_created.add(owner_username)

                        # Jika Profile sudah ada tapi role bukan OWNER, update
                        if not profile_created and owner_profile.role != 'OWNER':
                            owner_profile.role = 'OWNER'
                            owner_profile.save()
                            roles_updated.add(owner_username)

                    else:
                        # Fallback jika kolom owner_username kosong
                        owner_profile = fallback_owner_profile

                    # 3. Handle ForeignKeys (City & Category)
                    city_obj, _ = City.objects.get_or_create(name=row['lokasi_kota'])
                    category_obj, _ = Category.objects.get_or_create(name=row['kategori_olahraga'])

                    # 4. Handle harga
                    harga = row.get('harga_per_jam')
                    harga_bersih = int(float(harga)) if harga else None

                    # 5. Buat atau Update Venue (owner sekarang pakai owner_profile)
                    _, venue_created_flag = Venue.objects.update_or_create(
                        name=row['nama'],
                        defaults={
                            'owner': owner_profile, # <-- GUNAKAN OBJEK PROFILE
                            'price': harga_bersih,
                            'city': city_obj,
                            'category': category_obj,
                            'type': row['tipe'],
                            'address': row['alamat'],
                            'description': row['deskripsi'],
                            'image_url': row['link_gambar']
                        }
                    )

                    if venue_created_flag: venues_created += 1
                    else: venues_updated += 1

                self.stdout.write(self.style.SUCCESS('--- Impor Selesai! ---'))
                self.stdout.write(f'{venues_created} venue baru dibuat.')
                self.stdout.write(f'{venues_updated} venue di-update.')

                if users_created:
                    self.stdout.write(self.style.WARNING(f'\nUser baru berikut dibuat (tanpa password): {", ".join(users_created)}'))
                if profiles_created:
                     self.stdout.write(self.style.SUCCESS(f'Profile baru (role OWNER) dibuat untuk: {", ".join(profiles_created)}'))
                if roles_updated:
                     self.stdout.write(self.style.WARNING(f'Role Profile berikut diubah menjadi OWNER: {", ".join(roles_updated)}'))
                if users_created:
                    self.stdout.write(self.style.WARNING('Harap set password user baru di halaman Admin Django.'))


        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {file_path} tidak ditemukan.'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'ERROR: Header CSV tidak ditemukan: {e}.'))
            self.stdout.write(self.style.ERROR('Pastikan header CSV benar (nama, harga_per_jam, lokasi_kota, kategori_olahraga, tipe, alamat, deskripsi, link_gambar, owner_username).'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Terjadi error lain: {e}'))
            import traceback
            traceback.print_exc() # Print traceback for more details on other errors