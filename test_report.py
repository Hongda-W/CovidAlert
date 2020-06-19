from src.models.reports.report import Report

report = Report('CO')
report.load_data()
print(report.state_info)
print(report.json())
# report.save_to_mongo()
fig = report.plot_historic()

fig.savefig('test.png')
