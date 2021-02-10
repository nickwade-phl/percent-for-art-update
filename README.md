# percent-for-art-update

Three arcpy scripts that run in succession to update the working versions of the Percent for Art layers before they are added to DataBridge. 

1.	Staff from Urban Design or PHDC will notify you if they have edited a feature in the Percent for Art Excel document. To update the GIS layers, open G:\A STAFF\DanWhaland\PRA Percent for Art\Percent for Art with OneDrive\Percent for Art with OneDrive.aprx. This map contains the working version of the Percent for Art GIS layer (named
  “Percent_for_Art_Master”), which is joined to the OneDrive Excel document that is serving as a temporary database (shown as “Percent_for_Art_Master_Table$” in the Pro document).
  
2.	If the map contains the Percent_for_Art_Enterprise_rev, Percent_for_Art_Public_rev, GIS_PLANNING.Percent_for_Art_Public or GIS_PLANNING.Percent_for_Art_Enterprise layers,
  remove them from the map. 
  
3.	Use the following workflow to update the working versions of the Percent for Art layers:
    a.	From the Python window, load in and run update_first_part.py. 
    b.	Remove Percent_for_Art_Enterprise_rev from the Contents pane.
    c.	From the Python window, load in and run update_second_part.py
    d.	Remove Percent_for_Art_Enterprise_rev from the Contents pane.
    e.	From the Python window, load in and run update_third_part.py
    4.	Truncate/append: Use the Truncate tool on the DataBridge versions of the layers (GIS_PLANNING.Percent_for_Art_Public and GIS_PLANNING.Percent_for_Art_Enterprise). Then use 
        the append tool on those layers to append Percent_for_Art_Enterprise_rev and Percent_for_Art_Public_rev to the appropriate DataBridge layers. 
