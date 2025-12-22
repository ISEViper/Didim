import pandas as pd
from django.core.management.base import BaseCommand
from finance.models import GoldPrice, SilverPrice
from decimal import Decimal


class Command(BaseCommand):
    help = '금/은 시세 엑셀 데이터 import'

    def add_arguments(self, parser):
        parser.add_argument('--gold', type=str, help='금 시세 엑셀 파일 경로')
        parser.add_argument('--silver', type=str, help='은 시세 엑셀 파일 경로')

    def handle(self, *args, **options):
        if options['gold']:
            self.import_gold(options['gold'])
        if options['silver']:
            self.import_silver(options['silver'])

    def parse_price(self, value):
        """가격 문자열을 Decimal로 변환"""
        if pd.isna(value):
            return Decimal('0')
        if isinstance(value, str):
            return Decimal(value.replace(',', ''))
        return Decimal(str(value))

    def import_gold(self, filepath):
        self.stdout.write(f'금 시세 import 중: {filepath}')
        df = pd.read_excel(filepath)
        
        count = 0
        for _, row in df.iterrows():
            try:
                GoldPrice.objects.update_or_create(
                    date=row['Date'],
                    defaults={
                        'close_price': self.parse_price(row['Close/Last']),
                        'open_price': self.parse_price(row['Open']),
                        'high_price': self.parse_price(row['High']),
                        'low_price': self.parse_price(row['Low']),
                        'volume': self.parse_price(row['Volume']),
                    }
                )
                count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'금 시세 {count}개 import 완료'))

    def import_silver(self, filepath):
        self.stdout.write(f'은 시세 import 중: {filepath}')
        df = pd.read_excel(filepath)
        
        count = 0
        for _, row in df.iterrows():
            try:
                # Open 컬럼 데이터 처리 (날짜가 들어간 경우 처리)
                open_price = row['Open']
                if pd.isna(open_price) or isinstance(open_price, pd.Timestamp):
                    open_price = row['Close/Last']
                
                SilverPrice.objects.update_or_create(
                    date=row['Date'],
                    defaults={
                        'close_price': self.parse_price(row['Close/Last']),
                        'open_price': self.parse_price(open_price),
                        'high_price': self.parse_price(row['High']),
                        'low_price': self.parse_price(row['Low']),
                        'volume': self.parse_price(row['Volume']),
                    }
                )
                count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'은 시세 {count}개 import 완료'))