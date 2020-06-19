from src.models.reports.report import Report
import io, base64

report = Report('CO')
report.load_data()
print(report.state_info)
print(report.json())
# report.save_to_mongo()
fig = report.plot_historic()

img = io.BytesIO()
fig.savefig(img, format='png')
img.seek(0)
plot_url = base64.b64encode(img.getvalue()).decode()

print(len(plot_url))
print(plot_url[:500])