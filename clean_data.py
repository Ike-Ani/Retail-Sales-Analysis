import pandas as pd

class CleanData:
    def __init__(self, filepath=None, df=None):
        self.data = None
        if filepath:
            self.data = pd.read_csv(filepath)
        elif df is not None:
            self.data = df.copy()
        else:
            raise ValueError('filepath or df must be provided')

    def drop_invalid_rows(self):
        """Remove rows where both Quantity and Total Spent are missing"""
        self.data = self.data.dropna(subset=['Quantity', 'Total Spent'], how='all')
        return self

    def fill_price_per_unit(self):
        """Calculate missing Price Per Unit from Total Spent / Quantity"""
        self.data['Price Per Unit'] = self.data['Price Per Unit'].fillna(
            self.data['Total Spent'] / self.data['Quantity']
        )
        return self

    def fill_item_column(self):
        """Fill missing Item based on Category and Price Per Unit"""
        default_items = self.data.groupby(['Category', 'Price Per Unit'])['Item'].transform(
            lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
        )

        # Fill missing values
        self.data['Item'] = self.data['Item'].fillna(default_items)
        return self

    def fill_discount_applied(self):
        """Fill missing Discount Applied based on most common discount per Item"""
        self.data['Discount Applied'] = self.data['Discount Applied'].fillna(
            self.data.groupby('Item')['Discount Applied'].transform(
                lambda x: x.mode()[0] if not x.mode().empty else False
            )
        )
        return self

    def fix_location(self):
        """Cash purchases should be IN-STORE ONLY"""
        self.data.loc[self.data['Payment Method'] == 'Cash', 'Location'] = 'In-store'
        return self

    def save(self, name):
        """Save cleaned data to CSV"""
        self.data.to_csv(name, index=False)
        return self

    def summary(self):
        """Show missing values per column"""
        return self.data.isnull().sum()

    def get_data(self):
        """Return the cleaned DataFrame"""
        return self.data