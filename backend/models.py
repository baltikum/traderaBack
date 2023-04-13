from django.db import models



class Auctions(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.CharField(max_length=255)
    item_url = models.CharField(max_length=255)
    price = models.IntegerField(null=True, blank=True)
    total_bids = models.IntegerField(default=0)
    seller_alias = models.CharField(max_length=255, null=True, blank=True)
    search_term = models.CharField(max_length=255)
    auction_category = models.IntegerField(default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    auction_type = models.BooleanField(default=True)
    new_item = models.BooleanField(default=True)
    ending_soon = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    bidding_on = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Searches(models.Model):
    id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=255)
    category = models.IntegerField(default=0)
    average_price = models.IntegerField(null=True, blank=True)
    highest_price = models.IntegerField(null=True, blank=True)
    lowest_price = models.IntegerField(null=True, blank=True)
    auctions = models.ManyToManyField(Auctions)
    def __str__(self):
        return self.term
    class Meta:
        unique_together = ['term', 'category']
    

class Biddings(models.Model):
    auction = models.OneToOneField(Auctions, on_delete=models.CASCADE, primary_key=True)
    highest_bid = models.IntegerField(null=True, blank=True)
    ends = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Bidding for {self.auction.name}"