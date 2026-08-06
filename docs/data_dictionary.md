# Data Dictionary - Enterprise Sales Dataset

This data dictionary describes the schema of the 100,000-row enterprise sales dataset generated for the **Business Growth Analytics Suite**.

| Column Name | Data Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `Order ID` | String | Unique identifier for each sales transaction | `ORD-2024-100005` |
| `Order Date` | Timestamp | Timestamp when transaction occurred | `2024-03-15 14:22:10` |
| `Customer ID` | String | Unique identifier for individual customer | `CUST-10482` |
| `Customer Name` | String | Full name of customer | `Aarav Sharma` |
| `City` | String | Commercial city where order was placed | `Mumbai` |
| `State` | String | Corresponding state for the city | `Maharashtra` |
| `Product` | String | Name of purchased product | `MacBook Pro 16-inch` |
| `Category` | String | Product category (`Technology`, `Furniture`, `Office Supplies`) | `Technology` |
| `Quantity` | Integer | Number of units purchased | `2` |
| `Unit Price` | Float | Price per single unit before discount | `219900.00` |
| `Discount` | Float | Discount percentage applied (0.00 to 0.25) | `0.10` |
| `Sales` | Float | Final sales revenue: `Quantity * Unit Price * (1 - Discount)` | `395820.00` |
| `Profit` | Float | Net profit earned after accounting for margins and overhead | `75205.80` |
| `Payment Method` | String | Channel used (`UPI`, `Credit Card`, `Net Banking`, `Debit Card`, `Cash on Delivery`) | `UPI` |
