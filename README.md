# Spatial-and-Temporal-Variance-of-Particulate-Matter-Across-Diverse-Micro-Environments-

Project Overview
Developed a low-cost, real-time particulate matter (PM) monitoring system to measure dust levels across 11 locations at the University of Colombo. The project examined how human activity, ventilation, and atmospheric conditions affect air quality, providing a practical alternative to expensive monitoring systems.

Key Contributions
• Hardware Engineering: Built a sensing system using the SHARP GP2Y1010AU0F dust sensor with an Arduino Nano for 1-second interval data collection.
• Sensor Calibration: Calibrated the sensor using a controlled smoke source to establish a voltage-to-dust density (mg/m³) relationship, with a baseline of ~0.38 V.
• Signal Processing: Applied a median filter (kernel size = 5) to reduce noise and remove signal spikes while preserving real-world variations.
• Data Analysis: Used statistical metrics such as standard deviation (σ = 0.0063), skewness (+1.28), and IQR to evaluate accuracy and environmental trends.
Key Insights
• Indoor spaces act as “dust traps,” with human activity increasing PM levels, especially in the afternoon due to poor ventilation.
• Outdoor environments showed the opposite trend, with morning inversion trapping dust and afternoon convection improving air dispersion.
• Demonstrated that low-cost sensors, combined with filtering and analysis, can deliver reliable environmental insights.

Tools & Technologies
Arduino Nano, SHARP Optical Dust Sensor, Infrared Light Scattering, ADC Data Acquisition, Median Filtering, Statistical Analysis, Linear Calibration Models
