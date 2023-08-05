# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/02_Merge_Data.ipynb (unless otherwise specified).

__all__ = ['mergeDatasets']

# Cell
# hide
# @title Run: Import Modules

# These imports will handle everything
import os
import sys
import csv
import numpy as np
import pandas as pd
pd.set_option('max_colwidth', 20)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)

# Cell
#@title Run: Create mergeDatasets()

# Geometry_DS = https://docs.google.com/spreadsheets/d/e/2PACX-1vTPKW6YOHPFvkw3FM3m5y67-Aa5ZlrM0Ee1Fb57wlGuldr99sEvVWnkej30FXhSb3j8o9gr8izq2ZRP/pub?output=csv
# Data_DS = https://docs.google.com/spreadsheets/d/e/2PACX-1vREwwa_s8Ix39OYGnnS_wA8flOoEkU7reIV4o3ZhlwYhLXhpNEvnOia_uHUDBvnFptkLLHHlaQNvsQE/pub?output=csv

# Import needed modules
import os, sys, csv, pandas as pd, numpy as np

def mergeDatasets(left_ds=False,
                  right_ds=False,
                  crosswalk_ds=False,
                  use_crosswalk = True,
                  left_col=False,
                  right_col=False,
                  crosswalk_left_col = False,
                  crosswalk_right_col = False,
                  merge_how=False,
                  interactive=True):

  # Decide to perform a merge or commit a pull
  def mergeOrPull(df, cw, left_on, right_on, how):

    def merge(df, cw, left_on, right_on, how):
      df = pd.merge(df, cw, left_on=left_on, right_on=right_on, how=how)
      # df.drop(left_on, axis=1)
      df[right_on] = df[right_on].fillna(value='empty')
      return df

    def pull(df, cw, left_on, right_on, how):
      crswlk = dict(zip(cw[right_on], cw[how]  ) )
      dtype = df[left_on].dtype
      if dtype =='object':  df[how] = df.apply(lambda row: crswlk.get(str(row[left_on]), "empty"), axis=1)
      elif dtype == 'int64':
        df[how] = df.apply(lambda row: crswlk.get(int(row[left_on]), "empty"), axis=1)
      return df

    mergeType = how in ['left', 'right', 'outer', 'inner']
    if mergeType: return merge(df, cw, left_on, right_on, how)
    else: return pull(df, cw, left_on, right_on, how)



  # Filter between matched records and not.
  def filterEmpties(df, cw, left_on, right_on, how, interactive):

    if how in ['left', 'right', 'outer', 'inner']: how = right_on
    nomatch = df.loc[df[how] == 'empty']
    nomatch = nomatch.sort_values(by=left_on, ascending=True)

    if nomatch.shape[0] > 0:
      # Do the same thing with our foreign tracts
      if(interactive): print('\n Local Column Values Not Matched ')
      if(interactive): print(nomatch[left_on].unique() )
      if(interactive): print(len(nomatch[left_on]))
      if(interactive): print('\n Crosswalk Unique Column Values')
      if(interactive): print(cw[right_on].unique() )

    # Create a new column with the tracts value mapped to its corresponding value from the crossswalk
    df[how].replace('empty', np.nan, inplace=True)
    df.dropna(subset=[how], inplace=True)
    # cw = cw.sort_values(by=how, ascending=True)
    return df

  # Check Crosswalk Params
  def handleCrosswalkDataset(crosswalk_ds, crosswalk_left_col, crosswalk_right_col, interactive):
    noDataset = (not isinstance(crosswalk_ds, pd.DataFrame))
    noColumns = (not crosswalk_left_col or not crosswalk_right_col)
    columnDne = checkColumns(crosswalk_ds, crosswalk_left_col)
    columnDne = checkColumns(crosswalk_ds, crosswalk_right_col)
    if ( noDataset or noColumns ): return mergeDatasets( *getMergeParams() );



  def handleMergeHow(right_ds, merge_how, interactive):
    howList = ['left', 'right', 'outer', 'inner']
    mergeHowInHowList = merge_how in howList
    mergeHowInRightDf = checkColumns(right_ds, merge_how)
    mergeHowExists = (mergeHowInRightDf or mergeHowInHowList)
    if ( mergeHowExists ): return merge_how
    elif ( not interactive): return False
    else:
      try:
        print('Valid Column Not Given');
        print("\n 1) Pull A single Column from the Right Dataset: ", right_ds.columns)
        print("OR");
        print("2) Join Operation: (‘left’, ‘right’, ‘outer’, ‘inner’, columnName) " )
        print("\n Please select a value from either list");
        merge_how = input("Column Name: " )
        return handleMergeHow(right_ds, merge_how, interactive);
      except: return handleMergeHow(right_ds, merge_how, interactive);



  def processColumn(df, col, interactive):
    # Check Column in Dataset
    colExists = checkColumns(df, col)
    noColNotInteractive = not colExists and not interactive
    if colExists: return col
    elif (noColNotInteractive): return False
    else:
        try:
          print('Valid Column Not Given');
          print(df.columns)
          print(df.head())
          print("Please provide a dataset column name from the list above.");
          col = input("Column Name: " )
          colExists = checkColumns(df, col)
          if (colExists): return col
          else: return processColumn(df, col, interactive);
        except: return processColumn(df, col, interactive);






  # Returns a DF if provided a DF or URL. False otherwise.
  def retrieveDatasetFromUrl(df):
    datasetExists = checkDataSetExists(df)
    urlGiven = df and not datasetExists
    if datasetExists: return df
    elif ( urlGiven ):
      try:
        urlGiven = df
        df = pd.read_csv( df )
        datasetExists = checkDataSetExists(df)
        if datasetExists: return df
      except: return False;
    else: return False

  # If !DF and interactive, re-processDataset. False otherwise.
  def retrieveUrlForDataset(df, interactive):
    dsExists = checkDataSetExists(df)
    if( dsExists ): return df
    if ( not dsExists and not interactive): return False;
    if ( not dsExists and interactive):
      df = input("Please provide a new dataset URL: " );
      return processDataset(df, interactive)

  # Ensures a Pandas DF is returned.
  # If not Interactive, may return FALSE.
  def processDataset(df, interactive):
    # Returns a DF if provided a DF or URL. False otherwise.
    df = retrieveDatasetFromUrl(df)
    # If !DF and interactive, re-processDataset w/a new URL
    df = retrieveUrlForDataset(df, interactive)
    return df





  # Check Dataset Params
  def handleDatasetAndColumns(df, col, interactive):
    dfStatus = colStatus = True
    # Ensure A Dataset is being handled
    df = processDataset(df, interactive)
    if ( not checkDataSetExists(df) ): dfStatus = False

    # Ensure A Column Exists
    col = processColumn(df, col, interactive)
    if ( col == False ): colStatus = False
    return df, col, dfStatus, colStatus




  # Ensure data types are the same
  def coerceDtypes(left_ds, right_ds, left_col, right_col, interactive):
    status = False
    foreignDtype = right_ds[right_col].dtype
    localDtype = left_ds[left_col].dtype

    localIsNumber = localDtype == 'float64' or localDtype == 'int64'
    foreignIsNumber = foreignDtype == 'int64' or foreignDtype == 'int64'

    if foreignIsNumber: right_ds[right_col] = right_ds[right_col].fillna(-1321321321321325)
    if localIsNumber: left_ds[left_col] = left_ds[left_col].fillna(-1321321321321325)

    # Coerce one way or the other if possible
    if localIsNumber and foreignDtype == 'object':
      if(interactive): print('Converting Foreign Key from Object to Int' )
      right_ds[right_col] = pd.to_numeric(right_ds[right_col], errors='coerce')

    if localDtype == 'object' and foreignIsNumber:
      if(interactive):  print('Converting Foreign Key from Object to Int' )
      left_ds[left_col] = pd.to_numeric(left_ds[left_col], errors='coerce')

    # Coerce INTS AND FLOATS if possible
    if localDtype == 'int64' and foreignDtype == 'float64':
      if(interactive): print('Converting Local Key from Int to float' )
      right_ds[right_col] = right_ds[right_col].astype(int)

    if localDtype == 'float64' and foreignDtype == 'int64':
      if(interactive): print('Converting Local Key from float64 to Int' )
      left_ds[left_col] = left_ds[left_col].astype(int)

    foreignDtype = right_ds[right_col].dtype
    localDtype = left_ds[left_col].dtype

    # Return the data and the coerce status
    if localDtype == foreignDtype: status = True
    return left_ds, right_ds, status




  # Check if the columns actually exist
  def checkColumns(dataset, column): return {column}.issubset(dataset.columns)
  # Check if the DataSet actually exist
  def checkDataSetExists(df): return isinstance(df, pd.DataFrame)

  # This function uses all the other functions
  def main(left_ds, right_ds, crosswalk_ds, use_crosswalk, left_col, right_col,
           crosswalk_left_col, crosswalk_right_col, merge_how, interactive):

    if(interactive):print('\n Handling Left Dataset');
    left_ds, left_col, dfStatus, colStatus = handleDatasetAndColumns(left_ds, left_col, interactive)
    if ( dfStatus and colStatus and interactive):
      print('Left Dataset and Columns are Valid');
    elif( not (dfStatus and colStatus) and not interactive):
      return 'ERROR: Error with Left Dataset and or Column'

    if(interactive):print('\n Handling Right Dataset');
    right_ds, right_col, dfStatus, colStatus  = handleDatasetAndColumns(right_ds, right_col, interactive)
    if ( dfStatus and colStatus and interactive):
      print('Right Dataset and Columns are Valid');
    elif( not (dfStatus and colStatus) and not interactive):
      return 'ERROR: Error with Right Dataset and or Column'

    if(interactive):print('\n Checking the merge_how Parameter');
    merge_how = handleMergeHow(right_ds, merge_how, interactive)
    if ( merge_how and interactive): print('merge_how operator is Valid', merge_how)
    elif( not  merge_how and not interactive ): return 'ERROR: Error with merge_how Paramter'

    # Returns true if a DF. False if URL
    crosswalkSupplied = checkDataSetExists(crosswalk_ds)
    if not crosswalkSupplied and isinstance(crosswalk_ds, str): crosswalkSupplied = True
    if (interactive and use_crosswalk):
      if(interactive): print('\n Checking the Crosswalk Parameter');
      if(not crosswalkSupplied):
        use_crosswalk = input("Are you using a crosswalk? 'True' or 'False': " )
        use_crosswalk = use_crosswalk == "True"
    else: use_crosswalk = crosswalkSupplied

    # If a user is using a crosswalk, then assess match for left-cw, and right-cw.
    if( use_crosswalk ):
      # This will load our dataset if provided as a url.
      if(interactive):print('\n Handling Crosswalk Left Dataset Loading');
      crosswalk_ds_discard, crosswalk_left_col, dfStatus, colStatus = handleDatasetAndColumns(crosswalk_ds, crosswalk_left_col, interactive)
      # the first Item is our Dataset, which we discard the first time this data is called, kept the second.
      if(interactive):print('\n Handling Crosswalk Right Dataset Loading');
      crosswalk_ds, crosswalk_right_col, dfStatus, colStatus = handleDatasetAndColumns(crosswalk_ds, crosswalk_right_col, interactive)
      if(interactive):print('\n Assessment Completed');

      if(interactive): print('\n Ensuring Left->Crosswalk compatability')
      left_ds, crosswalk_ds, status = coerceDtypes(left_ds, crosswalk_ds, left_col, crosswalk_left_col, interactive);
      if(interactive): print('\n Ensuring Crosswalk->Right compatability')
      right_ds, crosswalk_ds, status = coerceDtypes(right_ds, crosswalk_ds, right_col, crosswalk_right_col, interactive);
    # If a user is not using a crswk, then assess match for left-right.
    else:
      if(interactive): print('\n Ensuring Left->Right compatability')
      left_ds, right_ds, status = coerceDtypes(left_ds, right_ds, left_col, right_col, interactive);

    if( status == False and not interactive ):
      print('ERROR: Foreign keys data types do not match');
      return False;
    if( status == False and interactive ):
      print('Could not resolve differences in data types.')
      restart = input("Would you like to restart?: 'True' or 'False': " )
      restart = restart == "True"
      if restart : return mergeDatasets()
      else: print('GOODBYE'); return left_ds, right_ds

    else:
      if(use_crosswalk):
        if(interactive):
          print('PERFORMING MERGE LEFT->CROSSWALK');
          print('left_on', crosswalk_left_col, 'right_on', crosswalk_right_col, 'how', merge_how);
        # Perform the left-CW Merge using left_col, crosswalk_left_col then pull the crosswalk_right_col
        left_ds = mergeOrPull(left_ds, crosswalk_ds, left_col, crosswalk_left_col, crosswalk_right_col)
        # Filter out columns not matched
        left_ds = filterEmpties(left_ds, crosswalk_ds, left_col, crosswalk_left_col, crosswalk_right_col, interactive)
        # set the new left_col as the crosswalk_right_col since it will be able to match to the right_col
        left_col = crosswalk_right_col

      # If the crosswalk was needed, it has now been integrated in to the left table.
      # The crosswalk col corresponding to the right_col should exist in the left Table.
      # Merge the left and right tables now.

      if(interactive):
        print('PERFORMING MERGE LEFT->RIGHT');
        print('left_col', left_col, 'right_col', right_col, 'how', merge_how);
      # Perform the merge
      left_ds = mergeOrPull(left_ds, right_ds, left_col, right_col, merge_how)
      # Filter out columns not matched
      left_ds = filterEmpties(left_ds, right_ds, left_col, right_col, merge_how, interactive)

    return left_ds

  return main( left_ds, right_ds, crosswalk_ds, use_crosswalk, left_col, right_col, crosswalk_left_col, crosswalk_right_col, merge_how, interactive )
