# second part
import arcpy

# Set workspace
arcpy.env.workspace = "G:/A_STAFF/DanWhaland/PRA Percent for Art/PRA_P4A_Final.gdb"

# Allow overwrite of existing files
arcpy.env.overwriteOutput = 'TRUE'

# Create variables
Master_P4A = "Percent_for_Art_Master"
New_P4A_Public = "Percent_for_Art_Public_rev"
New_P4A_Enterprise = "Percent_for_Art_Enterprise_rev"

# Add Date_1 field
arcpy.AddField_management(New_P4A_Enterprise, "Date_1", field_type="TEXT", field_length=255)

# calculate the new date field
arcpy.CalculateField_management(New_P4A_Enterprise, "Date_1", '!Date_!', "PYTHON3")

# Delete old date field
arcpy.DeleteField_management(New_P4A_Enterprise, "Date_")

# Alter Date_1 to make it Date_
arcpy.AlterField_management(New_P4A_Enterprise, "Date_1", "Date_")