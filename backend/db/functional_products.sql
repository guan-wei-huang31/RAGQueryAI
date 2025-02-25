/*
Filename: functional_products.sql
Author: Guan-Wei Huang
Created: 2025-02-24
Version: 1.0.0
License: MIT
Description:
    This SQL script initializes the database schema and populates data 
    for functional products. It includes table creation, constraints, 
    indexes, and sample data.

Contact: gwhuang24@gmail.com
GitHub: https://github.com/guan-wei-huang31
*/


CREATE TABLE Functional_Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    weight DECIMAL(10,2) NOT NULL,
    manufacturer TEXT NOT NULL,
    expiration_date DATE NOT NULL,
    storage_method TEXT NOT NULL,
    delivery_time TEXT NOT NULL,
    reference_price DECIMAL(10,2) NOT NULL,
    allergy_info TEXT,
    in_stock INTEGER NOT NULL,  -- SQLite does not support BOOLEAN, use INTEGER (1 = TRUE, 0 = FALSE)
    certifications TEXT,
    health_description TEXT,
    product_details TEXT
);

INSERT INTO Functional_Products 
(product_name, weight, manufacturer, expiration_date, storage_method, delivery_time, reference_price, allergy_info, in_stock, certifications, health_description, product_details)
VALUES 
('High-Purity DHA Fish Oil', 60.00, 'Japan Health Food Co., Ltd.', '2026-05-12', 'Store in a cool, dry place away from sunlight', '7-10 days', 150.00, 'Contains fish-derived ingredients, not suitable for seafood allergy sufferers', 1, 'JAS Organic, GMP Certified', 'Supports memory enhancement and concentration', 'Each capsule contains 90% pure DHA, suitable for daily health maintenance'),
('Probiotic Fermented Powder', 200.00, 'Taiwan Biotech Co., Ltd.', '2025-12-01', 'Keep sealed in a dry place', '5-7 days', 80.00, 'Contains dairy ingredients, not suitable for lactose-intolerant individuals', 1, 'HACCP, ISO22000', 'Maintains gut health and improves digestion', 'Made with natural fermentation technology and multiple probiotic strains'),
('Chlorella Protein Powder', 500.00, 'Green Energy Nutrition Inc.', '2026-08-15', 'Store at room temperature, avoid humidity', '10-14 days', 120.00, 'Contains trace amounts of seaweed components', 1, 'USDA Organic, NON-GMO', 'Boosts immunity and provides essential amino acids and minerals', 'A plant-based protein source suitable for vegetarians'),
('Herbal Melatonin Tablets', 30.00, 'Natural Biotech Development Co.', '2027-02-20', 'Store in a cool, dry place away from direct sunlight', '3-5 days', 90.00, 'Contains herbal extracts, may cause allergic reactions in some individuals', 0, 'ECOCERT Natural Product Certified', 'Promotes sleep and improves sleep quality', 'Derived from natural plant extracts, free from artificial additives'),
('Collagen Peptide Powder', 250.00, 'Beauty & Health Technology Ltd.', '2025-11-30', 'Keep in a dry and cool place', '5-8 days', 200.00, 'Contains fish collagen, not suitable for seafood allergy sufferers', 1, 'FSSC22000, GMP Certified', 'Enhances skin elasticity and hydration', 'Highly absorbable small peptide molecules, suitable for mixing with drinks or food');
