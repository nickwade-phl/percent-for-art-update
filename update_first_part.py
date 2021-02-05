# first part
import arcpy

# Set workspace
arcpy.env.workspace = "G:/A_STAFF/DanWhaland/PRA Percent for Art/PRA_P4A_Final.gdb"

# Allow overwrite of existing files
arcpy.env.overwriteOutput = 'TRUE'

# Since arcpy.env.overwriteOutput does not seem to be working in ArcPro 2.4, use this line to delete the two _rev layers before creating them again
if arcpy.Exists("Percent_for_Art_Enterprise_rev"):
    arcpy.Delete_management("Percent_for_Art_Enterprise_rev")

if arcpy.Exists("Percent_for_Art_Public_rev"):
    arcpy.Delete_management("Percent_for_Art_Public_rev")

# Create variables
Master_P4A = "Percent_for_Art_Master"
New_P4A_Public = "Percent_for_Art_Public_rev"
New_P4A_Enterprise = "Percent_for_Art_Enterprise_rev"

# first, copy all the features from master to enterpise_rev. rename fields, remove fields, etc. THEN, select the Active features and copy them to public_rev
arcpy.CopyFeatures_management(Master_P4A, New_P4A_Enterprise)

# Copy values from old Image field to new Image field
arcpy.CalculateField_management(New_P4A_Enterprise, 'Newer_ImageField', '!Percent_for_Art_Master_Table__Image!', "PYTHON3")

# Change field names to match metadata 
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_P4A_ID", "P4A_ID", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Status", "Status", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Artist", "Artist", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Title", "Title", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Date", "Date_", "Date")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Location_N", "Location_Name", "Location Name")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Address", "Address", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Location_1", "Location_Note", "Location Note")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Medium", "Medium", new_field_alias="", clear_field_alias="TRUE")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Neighborho", "Neighborhood", "Neighborhood")
arcpy.AlterField_management(New_P4A_Enterprise, "Percent_for_Art_Master_Table__Owner", "Owner", new_field_alias="", clear_field_alias="TRUE")

# Make a list of fields to delete at this point
dropFields = ["Percent_for_Art_Master_Artist","Percent_for_Art_Master_Title","Percent_for_Art_Master_Image","Percent_for_Art_Master_Table__P4A_ID","Percent_for_Art_Master_Table__OBJECTID","Percent_for_Art_Master_Table__ObjectID_1","Percent_for_Art_Master_Table__Shape_Leng","Percent_for_Art_Master_Table__Google_Str","Percent_for_Art_Master_Table__Note","Percent_for_Art_Master_Table__Image"]

# delete the fields in the list
arcpy.DeleteField_management(New_P4A_Enterprise, dropFields)

# Add field to host new Google field
arcpy.AddField_management(New_P4A_Enterprise, "Google_Streetview_Link", field_type="TEXT", field_length=500, field_alias="Google Street View Link")

# set variables to handle concatenate the google fields
expression = "reclass(!Percent_for_Art_Master_Table__FirstPartGoogle!,!Percent_for_Art_Master_Table__SecondPartGoogle!)"
codeblock = """
def reclass(FirstPartGoogle,SecondPartGoogle):
  return FirstPartGoogle + SecondPartGoogle
"""
arcpy.CalculateField_management(New_P4A_Enterprise, "Google_Streetview_Link", expression, "PYTHON3", codeblock)

# set variables to handle the #VALUE! values
badValexpression = "reclass(!Google_Streetview_Link!)"
badValCodeblock = """
def reclass(GoogleStreetView):
  if GoogleStreetView.startswith("#V"):
    return "N/A"
  else:
    return GoogleStreetView
"""

arcpy.CalculateField_management(New_P4A_Enterprise, "Google_Streetview_Link", badValexpression, "PYTHON3", badValCodeblock)

# Add Note field and assign the appropriate field_length (you can only define field length when you add a new field, not during calculate field or alter field)
arcpy.AddField_management(New_P4A_Enterprise, "Note", field_type="TEXT", field_length=350)

