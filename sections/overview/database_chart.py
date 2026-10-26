from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QToolTip
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from db import DatabaseManager

def create_database_chart_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("All User Databases Size Distribution")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #334155;")
    
    series = QPieSeries()
    
    db = DatabaseManager()
    query = """
        SELECT 
            d.name AS DatabaseName,
            CAST(SUM(mf.size) * 8.0 / 1024 AS DECIMAL(10,2)) AS SizeMB
        FROM sys.databases d
        JOIN sys.master_files mf ON d.database_id = mf.database_id
        WHERE d.database_id > 4
        GROUP BY d.name
        ORDER BY SizeMB DESC;
    """
    results = db.execute_query(query)
    
    # Tooltip handler function for slices
    def show_tooltip(status, db_name, size_mb):
        if status:
            QToolTip.showText(QCursor.pos(), f"Database: {db_name}\nSize: {size_mb} MB")
        else:
            QToolTip.hideText()

    if results:
        for record in results:
            db_name = str(record.get('DatabaseName') or record.get('databasename') or list(record.values())[0])
            size_mb = float(record.get('SizeMB') if 'SizeMB' in record else record.get('sizemb', list(record.values())[1]))
            if size_mb > 0:
                slice_item = series.append(db_name, size_mb)
                # Bind hover signal to show tooltip with specific db name and size
                slice_item.hovered.connect(lambda status, n=db_name, s=size_mb: show_tooltip(status, n, s))
    else:
        series.append("No Data", 1)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Storage Share by User DB (MB)")
    chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
    
    # Right-side legend alignment for clear viewing of all user databases
    if hasattr(Qt, 'AlignmentFlag'):
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
    chart.legend().setVisible(True)
    
    chart_view = QChartView(chart)
    chart_view.setRenderHint(chart_view.renderHints().Antialiasing)
    chart_view.setMouseTracking(True)
    chart_view.setStyleSheet("background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px;")
    
    layout.addWidget(title)
    layout.addWidget(chart_view)
    return widget