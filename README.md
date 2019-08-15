# Surfs-up-Hawaii!

<img src="./static/images/surfs-up.jpeg.png" alt="Surfs Up">

<p><strong>Ready for a trip to Hawaii? Better check the weather there before you go!</strong></p>

<p><code>Python</code> and <code>SQLAlchemy</code> were used to reflect tables from sqlite database files into SQLAlchemy ORM, to which queries were made with exploratory analysis on Hawaii climate being performed using <code>Pandas</code> library.</p>  

<p>Parameters taken into consideration were <em>precipitation in the latest 12 months</em>, <em>temperature recorded by the most active observation station</em>, <em>estimated average temperature for planned trip</em>, and <em>estimated daily normal temperatures for planned trip</em>. Results were visualized by <code>Matplotlib</code> as follows.</p>

<p><strong>Precipitation in the latest 12 months:</strong></p>
<img src="./static/images/prcp_1yr.png" alt="Precipitation">

<p><strong>Temperature recorded by the most active observation station:</strong></p>
<img src="./static/images/tobs_9281.png" alt="TObs9281">

<p><strong>Estimated average temperature for planned trip:</strong></p>
<img src="./static/images/trip_avg_temp.png" alt="Est Trip TAvg">

<p><strong>Estimated daily normal temperatures for planned trip:</strong></p>
<img src="./static/images/daily_normal_temperature.png" alt="Est Trip TDaily">

<p>Moreover, Flask API server was developed upon the aforementioned sqlite database files. Inqueries from customer and data returning thereafter were interfaced through HTML.</p>
<img src="./static/images/screenshot_api.png" alt="API Screenshot">
