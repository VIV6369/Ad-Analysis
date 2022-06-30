#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
#1 Examine the first few rows of ad_clicks.

ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks.head(10))

#2 Your manager wants to know which ad platform is getting you the most views.
# How many views (i.e., rows of the table) came from each utm_source?

most_views = ad_clicks.groupby('utm_source').user_id.count().reset_index()
print(most_views)

#3 If the column ad_click_timestamp is not null, then someone actually clicked on the ad that was displayed.
# Create a new column called is_click, which is True if ad_click_timestamp is not null and False otherwise.

ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()
print(ad_clicks)

#4 We want to know the percent of people who clicked on ads from each utm_source.
# Start by grouping by utm_source and is_click and counting the number of user_id‘s in each of those groups. 
# Save your answer to the variable clicks_by_source.

clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
print(clicks_by_source)

#5 Now let’s pivot the data so that the columns are is_click (either True or False), the index is utm_source, and the values are user_id.
# Save your results to the variable clicks_pivot.

clicks_pivot = clicks_by_source.pivot(
  columns = 'is_click',
  index = 'utm_source',
  values = 'user_id').reset_index()

print(clicks_pivot)

#6 Create a new column in clicks_pivot called percent_clicked which is equal to the percent of users who clicked on the ad from each utm_source.
# Was there a difference in click rates for each source?

clicks_pivot['percent_clicked'] = round(clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False]) *100, 2)
print(clicks_pivot)

#7 The column experimental_group tells us whether the user was shown Ad A or Ad B.
#Were approximately the same number of people shown both ads?

ad_shows = ad_clicks.groupby('experimental_group').user_id.count().reset_index()
print(ad_shows)

#8 Using the column is_click that we defined earlier, check to see if a greater percentage of users clicked on Ad A or Ad B.

most_clicked_ad = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()
most_clicked_ad_pivot = most_clicked_ad.pivot(
  columns = 'is_click',
  index = 'experimental_group',
  values = 'user_id').reset_index()
print(most_clicked_ad_pivot)

#9 The Product Manager for the A/B test thinks that the clicks might have changed by day of the week.
# Start by creating two DataFrames: a_clicks and b_clicks, which contain only the results for A group and B group, respectively.

a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

#10 For each group (a_clicks and b_clicks), calculate the percent of users who clicked on the ad by day.

# A clicks
a_clicks_by_day = a_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()
a_clicks_by_day_pivot = a_clicks_by_day.pivot(
  columns = 'is_click',
  index = 'day',
  values = 'user_id').reset_index()
a_clicks_by_day_pivot['percent_clicked'] = round(a_clicks_by_day_pivot[True] / (a_clicks_by_day_pivot[True] + a_clicks_by_day_pivot[False]) *100, 2)
print(a_clicks_by_day_pivot)

# B clicks
b_clicks_by_day = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()
b_clicks_by_day_pivot = b_clicks_by_day.pivot(
  columns = 'is_click',
  index = 'day',
  values = 'user_id').reset_index()
b_clicks_by_day_pivot['percent_clicked'] = round(b_clicks_by_day_pivot[True] / (b_clicks_by_day_pivot[True] + b_clicks_by_day_pivot[False]) *100, 2)
print(b_clicks_by_day_pivot)

#11 Compare the results for A and B. What happened over the course of the week?
# Do you recommend that your company use Ad A or Ad B?
# Use Ad A all days but Tuesday. Use Ad B on Tuesday.

