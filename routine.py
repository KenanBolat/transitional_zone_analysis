import numpy as np 
from pandas import DataFrame
import glob 

process_path = r"D:\WORKLOAD\001_HSAF\001_HSAF\products\merge_transitional_area_analysis"

days = [row for row in glob.glob1(process_path, "*_merged.tif")]

# buf_layer = "diff_mask_as_points_alps_Buf"

buf_layer = "diff_mask_as_points_buffer_0.20"
poi_layer = "diff_mask_as_points_alps"
mask_1_0 = arcpy.sa.Int(arcpy.sa.Plus(arcpy.sa.Con(arcpy.sa.IsNull("Diff_mask.tif"), 0 , "Diff_mask.tif"),'Mask_34.tif' ))
workdir = r"g:\sil"

df_mount = DataFrame()
df_flat = DataFrame()
for en, day in enumerate(days): 
	if en < 127: 
		continue
	print day, "is being calculated"
	doubleraster = day
	inraster_6 = arcpy.sa.Int(arcpy.sa.Times(mask_1_0, doubleraster))
	inraster_7 = arcpy.sa.Int(doubleraster)
	temp = []
	temp_tab_for_mount =  workdir + r'/temptab_mount'
	temp_tab_for_merge =  workdir + r'/temptab_merge'
	
	arcpy.sa.ZonalStatisticsAsTable(buf_layer, 'pointid', inraster_6, temp_tab_for_mount, "DATA", "ALL")
	df_temp_mount = DataFrame(arcpy.da.TableToNumPyArray(temp_tab_for_mount, "*"))
	df_temp_mount['date'] = datetime.datetime.strptime(doubleraster.split("_")[1], '%Y%m%d')
	df_mount = df_mount.append(df_temp_mount, ignore_index=True)
	
	arcpy.sa.ZonalStatisticsAsTable(poi_layer, 'pointid', inraster_7, temp_tab_for_merge, "DATA", "ALL")
	df_temp_flat = DataFrame(arcpy.da.TableToNumPyArray(temp_tab_for_merge, "*"))
	df_temp_flat['date'] = datetime.datetime.strptime(doubleraster.split("_")[1], '%Y%m%d')
	df_flat = df_flat.append(df_temp_flat, ignore_index=True)

df_flat.to_excel(r"g:\flat.xlsx")
df_mount.to_excel(r"g:\mount.xlsx")

# with arcpy.da.SearchCursor(buf_layer, ['pointid']) as rows:
# 	for en, row in enumerate(rows):
# 		fid = row[0]
# 		expression = '"pointid" = ' + str(fid)
# 		temp_shp = workdir + r'/tempshp' +  ".shp"
# 		arcpy.Select_analysis(buf_layer, temp_shp, expression)
# 		arcpy.sa.ZonalStatisticsAsTable(temp_shp, 'pointid', inraster, temp_tab, "DATA", "MAJORITY")

# 		for a in arcpy.da.SearchCursor(temp_tab, ['pointid', 'MAJORITY']):
# 			temp.append(a) 
# 		if en % 100 == 0 : 
# 			print fid, a 


# for a in arcpy.da.SearchCursor(temp_tab, ['pointid']):
# 	print a 
