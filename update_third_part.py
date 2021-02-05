# third part
import arcpy

# import smtplib for emails
import smtplib

# import os for environment variables
import os

# Set workspace
arcpy.env.workspace = "G:/A_STAFF/DanWhaland/PRA Percent for Art/PRA_P4A_Final.gdb"

# Allow overwrite of existing files
arcpy.env.overwriteOutput = 'TRUE'

# Create variables
Master_P4A = "Percent_for_Art_Master"
New_P4A_Public = "Percent_for_Art_Public_rev"
New_P4A_Enterprise = "Percent_for_Art_Enterprise_rev"

# calculate note field
arcpy.CalculateField_management(New_P4A_Enterprise, "Note", '!Percent_for_Art_Master_Table__FirstPartNote! + !Percent_for_Art_Master_Table__SecondPartNote!')

# another list of fields to delete at this point
moreDropFields = ["Percent_for_Art_Master_Table__FirstPartGoogle","Percent_for_Art_Master_Table__SecondPartGoogle","Percent_for_Art_Master_Table__FirstPartNote","Percent_for_Art_Master_Table__SecondPartNote"]

# Delete the fields in the list
arcpy.DeleteField_management(New_P4A_Enterprise, moreDropFields)

# Alter new Image field to rename it appropriately
arcpy.AlterField_management(New_P4A_Enterprise, "Newer_ImageField", "Image", new_field_alias="", clear_field_alias="TRUE", field_length=1600)

# Select Active, In Progress, and Inaccessible Status features so you can copy them to the public_rev layer
arcpy.SelectLayerByAttribute_management(New_P4A_Enterprise, "NEW_SELECTION", "Status = 'Active' Or Status = 'In Progress' Or Status = 'Inaccessible'", None)

# Copy active status features to public_rev
arcpy.CopyFeatures_management(New_P4A_Enterprise, New_P4A_Public)

# Delete fields that shouldn't be in the public layer
arcpy.DeleteField_management(New_P4A_Public, "Owner")
arcpy.DeleteField_management(New_P4A_Public, "Note")

# email variables
sender = os.environ.get('DPDAppsProd_Email')
receivers = [os.environ.get('Dan_Email')]
password = os.environ.get('DPDAppsProd_password') 

message = """Subject: Percent for Art Ready for Upload

The working versions of the Percent for Art layers have been updated and are ready for upload. 

-DPD GIS
"""

smtpObj = smtplib.SMTP(host='smtp.office365.com', port=587)
smtpObj.starttls()
smtpObj.login(sender,password)

# send the email 
smtpObj.sendmail(sender, receivers, message)
smtpObj.quit()
