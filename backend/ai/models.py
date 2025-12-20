from django.db import models

# Create your models here.
class StockAiAnalysis(models.Model):
    ticker = models.CharField(max_length=10, db_index=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Analysis: {self.ticker} ({self.created_at})"