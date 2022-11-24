import io

from django.conf import settings
from django.core.management import BaseCommand
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
FILE_NAME = 'database.ods'


class Command(BaseCommand):
    def handle(self, *args, **options):
        credentials = service_account.Credentials.from_service_account_file(
            settings.SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        request = service.files().export_media(
            fileId=settings.GOOGLE_DRIVE_FILE_ID,
            mimeType='application/vnd.oasis.opendocument.spreadsheet')

        file = io.FileIO(FILE_NAME, 'wb')
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
