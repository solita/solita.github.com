---
layout: post
title: An unexpected acquaintance? Data Validation in R
author: filipwastberg
excerpt: R is popular programming language and is famous for statistical analysis and stunning visualizations. But it is not limited to those tasks, here we take a look how it can be used to do data validation on a Snowflake database.
date: 2020-12-17 06:30:00 +0100
tags:
 - R
 - Data validation
 - Snowflake
 - ETL
---
Data Engineering is a common task for any Data Scientist. Sure, we
rarely do the “real” Data Engineering, e.g. loading data from a
business system into a relational database. Rather, we work with data 
that already is in a database, and sometimes (if we're lucky) is put there by a Data Engineer. 
We usually transform this data into an analytical format from which we can derive
aggregations, visualizations and statistical models. In the start of any
Data Science project these jobs may not be of any significant
concern but as your Data Science products get used more and more the
importance of your data will increase.

Therefore it might be a good idea to invest some time into data
validation. There are many frameworks for data validation in different
programming languages. But Data Scientists usually feel comfortable
using tools they know, such as R and Python. R is a popular functional
programming language for data analysis. However, even though data
analysis is what R is famous for, the language is turing complete and
can do a lot of things besides statistics. In this case we’ll use the R
package `pointblank` that have made data validation and data quality
controls ridiculously easy to do in R. And it’s not just easy, it’s
really pretty too. And I love pretty things.

Data can come in many formats, but for this blog post I’ll focus on
databases and especially the increasingly popular database `Snowflake`.

Once you have created an odbc-DSN for your database it's usually straight 
forward to connect to any database in R using the packages `odbc` and
`DBI`.

    library(DBI)
    library(odbc)

    con <- dbConnect(odbc(), "example_database")
    
The database we use here is populated with a couple of million rows of
district heating data and is a part of a [research project](https://smartenergi.org/datasciencebrava/) that Solita Sweden is assisting.
This means that the data cannot be processed in memory in R. Thankfully,
the arguably most popular data manipulation
package in R `dplyr` has a database backend that can translate R code
into SQL. This means that we don’t have to bother with more than one
data manipulation framework at a time. With that said, most Data
Scientists should know some SQL, because sometimes the translations
don’t work as expected. But in 95% of the cases you can write R code
instead of SQL, which usually saves me a lot of time.

For instance, if I want to calculate how many observations there in a table and
group the result by a column I can use `dplyr` code on a database table:

    library(tidyverse) ## dplyr is included in the package tidyverse
    library(dbplyr)
    
    metering_tbl <- tbl(con, in_schema("PUBLIC", "METERING_READINGS_TBL"))

    ## Use dplyr code on the database table
    property_tbl <- metering_tbl %>% 
      group_by(PROPERTY, UNIT_OF_MEASURE) %>% 
      summarise(
        n = n(),
        mean_value = mean(VALUE),
        sd_value = sd(VALUE)
      )

    property_tbl

    ## Warning: Missing values are always removed in SQL.
    ## Use `mean(x, na.rm = TRUE)` to silence this warning
    ## This warning is displayed only once per session.

    ## # Source:   lazy query [?? x 5]
    ## # Database: Snowflake 4.40.1[filipw@Snowflake/xxx]
    ## # Groups:   PROPERTY
    ##   PROPERTY           UNIT_OF_MEASURE         n mean_value sd_value
    ##   <chr>              <chr>               <dbl>      <dbl>    <dbl>
    ## 1 return_temperature c               219273351       37.5   3118. 
    ## 2 flow_temperature   c               223159867       66.2     52.4
    ## 3 energy             MWh             116629833     6858.  768893. 
    ## 4 flow               m3              132111599     1837.  961871.

On the backend R sends SQL-code to Snowflake and returns the result. We
can see the SQL code generated:

    show_query(property_tbl)

    ## <SQL>
    ## SELECT "PROPERTY", "UNIT_OF_MEASURE", COUNT(*) AS "n", AVG("VALUE") AS "mean_value", STDDEV_SAMP("VALUE") AS "sd_value"
    ## FROM PUBLIC.METERING_READINGS_TBL
    ## GROUP BY "PROPERTY", "UNIT_OF_MEASURE"

When we’ve aggregated all these million rows we can import the data into
R and do all the things R is great for: visualizations, statistical
modeling and reporting.

But this post is not about that, rather we’ll use R for something it is
not famous for, but really good at: data validation.

The package [`pointblank`](https://github.com/rich-iannone/pointblank) is one of many data validation packages in R,
check out [`assertr`](https://github.com/ropensci/assertr), [`validate`](https://github.com/data-cleaning/validate) and [`dataMaid`](https://github.com/ekstroem/dataMaid) for other examples.

However, I’ve been extremely impressed by the work of the creator behind
`pointblank` *Rich Iannone*. The documentation of `pointblank` is really
something special. Furthermore, the time spent on tests in the package
give us an indication of the ambition behind the package, there are more
than 3000 unit tests for this package.

Anyways, let’s get down to it. You can use `pointblank` on data in
memory (maybe data comes from a csv-file or a json-file), but since
`pointblank` leverages the `dplyr` SQL backend you can also use it on
database tables.

So let's do that. We can start by taking a look at a database table in our database.
This table consist of hourly observations of [District Heating](https://en.wikipedia.org/wiki/District_heating) consumption. 
Data is imported from a District Heating network on a daily basis. It comes in JSON but I have
an R-script that transforms it into a table that can be used for statistical analysis.
Since the original format is in JSON there is a risk that the format might change,
so data validation of this table seems like a natural step.

    tbl(con, in_schema("PUBLIC", "METERING_READINGS_TBL")) %>% 
      select(-SOURCE_INSTANCE_NAME)

    ## # Source:   lazy query [?? x 6]
    ## # Database: Snowflake 4.40.1[filipw@Snowflake/xxx]
    ##    IMPORT_TIMESTAMP    TIMESTAMP           METERING_POINT_… PROPERTY
    ##    <dttm>              <dttm>              <chr>            <chr>   
    ##  1 2020-10-31 02:43:48 2020-07-04 12:00:00 cf767121-4f64-4… flow_te…
    ##  2 2020-10-31 02:43:48 2020-07-04 12:00:00 cf767121-4f64-4… return_…
    ##  3 2020-10-31 02:43:48 2020-07-04 13:00:00 cf767121-4f64-4… flow_te…
    ##  4 2020-10-31 02:43:48 2020-07-04 13:00:00 cf767121-4f64-4… return_…
    ##  5 2020-10-31 02:43:48 2020-07-04 14:00:00 cf767121-4f64-4… flow_te…
    ##  6 2020-10-31 02:43:48 2020-07-04 14:00:00 cf767121-4f64-4… return_…
    ##  7 2020-10-31 02:43:48 2020-07-04 15:00:00 cf767121-4f64-4… flow_te…
    ##  8 2020-10-31 02:43:48 2020-07-04 15:00:00 cf767121-4f64-4… return_…
    ##  9 2020-10-31 02:43:48 2020-07-04 16:00:00 cf767121-4f64-4… flow_te…
    ## 10 2020-10-31 02:43:48 2020-07-04 16:00:00 cf767121-4f64-4… return_…
    ## # … with more rows, and 2 more variables: UNIT_OF_MEASURE <chr>, VALUE <dbl>

In `pointblank` we first create an `agent` that defines which table we
want to validate. Then we use a `validation function` (these can also be
tests and expectations) to do our validation, e.g. `col_is_character()`.
Lastly we use the function `interrogate()` to do the actual validation.

So for this table we might be interested in checking the format of the
columns:

    library(pointblank)
    agent <- 
      create_agent(
          read_fn = ~tbl(con, in_schema("PUBLIC", "METERING_READINGS_TBL")),
          tbl_name = "METERING_READINGS_TBL"
        ) %>%
      col_is_character(vars(METERING_POINT_ID, PROPERTY, UNIT_OF_MEASURE)) %>% 
      col_is_numeric(vars(VALUE))%>%
      col_is_posix(vars(IMPORT_TIMESTAMP, TIMESTAMP)) %>% 
      interrogate()

When the “interrogation” is completed we can print the agent and we’ll
get a pretty table telling us what has happened.

    agent

<!--html_preserve-->
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
@import url("https://unpkg.com/balloon-css/balloon.min.css");
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap");
html {
  font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', 'Fira Sans', 'Droid Sans', Arial, sans-serif;
}

#report .gt_table {
  display: table;
  border-collapse: collapse;
  margin-left: auto;
  margin-right: auto;
  color: #333333;
  font-size: 90%;
  font-weight: normal;
  font-style: normal;
  background-color: #FFFFFF;
  width: auto;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #A8A8A8;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #A8A8A8;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
}

#report .gt_heading {
  background-color: #FFFFFF;
  text-align: center;
  border-bottom-color: #FFFFFF;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#report .gt_title {
  color: #333333;
  font-size: 125%;
  font-weight: initial;
  padding-top: 4px;
  padding-bottom: 4px;
  border-bottom-color: #FFFFFF;
  border-bottom-width: 0;
}

#report .gt_subtitle {
  color: #333333;
  font-size: 85%;
  font-weight: initial;
  padding-top: 0;
  padding-bottom: 4px;
  border-top-color: #FFFFFF;
  border-top-width: 0;
}

#report .gt_bottom_border {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#report .gt_col_headings {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#report .gt_col_heading {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  overflow-x: hidden;
}

#report .gt_column_spanner_outer {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
}

#report .gt_column_spanner_outer:first-child {
  padding-left: 0;
}

#report .gt_column_spanner_outer:last-child {
  padding-right: 0;
}

#report .gt_column_spanner {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  overflow-x: hidden;
  display: inline-block;
  width: 100%;
}

#report .gt_group_heading {
  padding: 8px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
}

#report .gt_empty_group_heading {
  padding: 0.5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: middle;
}

#report .gt_from_md > :first-child {
  margin-top: 0;
}

#report .gt_from_md > :last-child {
  margin-bottom: 0;
}

#report .gt_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 10px;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  overflow-x: hidden;
}

#report .gt_stub {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 12px;
}

#report .gt_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#report .gt_first_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
}

#report .gt_grand_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#report .gt_first_grand_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: double;
  border-top-width: 6px;
  border-top-color: #D3D3D3;
}

#report .gt_striped {
  background-color: rgba(128, 128, 128, 0.05);
}

#report .gt_table_body {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#report .gt_footnotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#report .gt_footnote {
  margin: 0px;
  font-size: 90%;
  padding: 4px;
}

#report .gt_sourcenotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#report .gt_sourcenote {
  font-size: 90%;
  padding: 4px;
}

#report .gt_left {
  text-align: left;
}

#report .gt_center {
  text-align: center;
}

#report .gt_right {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

#report .gt_font_normal {
  font-weight: normal;
}

#report .gt_font_bold {
  font-weight: bold;
}

#report .gt_font_italic {
  font-style: italic;
}

#report .gt_super {
  font-size: 65%;
}

#report .gt_footnote_marks {
  font-style: italic;
  font-size: 65%;
}

#pb_information {
  -webkit-font-smoothing: antialiased;
}

#report .gt_row {
  overflow: visible;
}

#report .gt_sourcenote {
  height: 35px;
  padding: 0;
}

#report code {
  font-family: 'IBM Plex Mono', monospace, courier;
  font-size: 11px;
  background-color: transparent;
  padding: 0;
}
</style>
<div id="report" style="overflow-x:auto;overflow-y:auto;width:auto;height:auto;">
<table class="gt_table" style="table-layout: fixed;; width: 0px">
<colgroup>
<col style="width:6px;"/>
<col style="width:35px;"/>
<col style="width:190px;"/>
<col style="width:120px;"/>
<col style="width:120px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:30px;"/>
<col style="width:30px;"/>
<col style="width:30px;"/>
<col style="width:65px;"/>
</colgroup>
<thead class="gt_header">
<tr>
<th colspan="14" class="gt_heading gt_title gt_font_normal" style="color: #444444; font-size: 28px; text-align: left; font-weight: 500;">
Pointblank Validation
</th>
</tr>
<tr>
<th colspan="14" class="gt_heading gt_subtitle gt_font_normal gt_bottom_border" style="font-size: 12px; text-align: left;">
<span
style="text-decoration-style:solid;text-decoration-color:#ADD8E6;text-decoration-line:underline;text-underline-position:under;color:#333333;font-variant-numeric:tabular-nums;padding-left:4px;margin-right:5px;padding-right:2px;">\[2020-12-04|16:02:03\]</span>
</p>

<span
style="background-color:#E2E2E2;color:#222222;padding:0.5em 0.5em;position:inherit;text-transform:uppercase;margin:5px 0px 5px 5px;font-weight:bold;border:solid 1px #E2E2E2;padding:2px 15px 2px 15px;font-size:smaller;"></span>
<span
style="background-color:none;color:#222222;padding:0.5em 0.5em;position:inherit;margin:5px 10px 5px -4px;font-weight:bold;border:solid 1px #E2E2E2;padding:2px 15px 2px 15px;font-size:smaller;">METERING\_READINGS\_TBL</span>

</th>
</tr>
</thead>
<thead class="gt_col_headings">
<tr>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
STEP
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
COLUMNS
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
VALUES
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
TBL
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
EVAL
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
⋅ ⋅ ⋅
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
PASS
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
FAIL
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
W
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
S
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
N
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
EXT
</th>
</tr>
</thead>
<tbody class="gt_table_body">
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
1
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_character" transform="translate(-0.397206, 0.151308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="c" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="39.9695669" y="43.0146694">c</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_character()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>METERING\_POINT\_ID</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
2
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_character" transform="translate(-0.397206, 0.151308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="c" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="39.9695669" y="43.0146694">c</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_character()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>PROPERTY</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
3
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_character" transform="translate(-0.397206, 0.151308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="c" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="39.9695669" y="43.0146694">c</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_character()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>UNIT\_OF\_MEASURE</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
4
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs></defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_numeric" transform="translate(-0.397206, 0.359210)">
<path d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z" id="rectangle" stroke="#000000" stroke-width="2"></path>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="d" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="38.4461294" y="43.0146694">d</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_numeric()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>VALUE</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
5
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_posix" transform="translate(-0.397206, 0.785474)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="T" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="38.4080435" y="43.0146694">T</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_posix()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>IMPORT\_TIMESTAMP</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
6
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_posix" transform="translate(-0.397206, 0.785474)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="T" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="38.4080435" y="43.0146694">T</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_posix()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>TIMESTAMP</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
</tbody>
<tfoot class="gt_sourcenotes">
<tr>
<td class="gt_sourcenote" colspan="14">
<span
style="background-color: #FFF;color: #444;padding: 0.5em 0.5em;position: inherit;text-transform: uppercase;margin-left: 10px;border: solid 1px #999999;font-variant-numeric: tabular-nums;border-radius: 0;padding: 2px 10px 2px 10px;font-size: smaller;">2020-12-04
16:02:10 CET</span><span
style="background-color: #FFF;color: #444;padding: 0.5em 0.5em;position: inherit;margin: 5px 1px 5px 0;border: solid 1px #999999;border-left: none;font-variant-numeric: tabular-nums;border-radius: 0;padding: 2px 10px 2px 10px;font-size: smaller;">1.9
s</span><span
style="background-color: #FFF;color: #444;padding: 0.5em 0.5em;position: inherit;text-transform: uppercase;margin: 5px 1px 5px -1px;border: solid 1px #999999;border-left: none;border-radius: 0;padding: 2px 10px 2px 10px;font-size: smaller;">2020-12-04
16:02:12 CET</span>
</td>
</tr>
</tfoot>
</table>
</div>
<!--/html_preserve-->

Another useful feature is to define actions with `action_level()` to
decide what should happen if a validation function fails. For instance,
we might want to check that all the dates in our table are within a
certain range, and if they’re not we’d like to either add a *warning* or
if the amount of fail exceeds a certain limit we’d like to *stop*.

Below I've added a validation function to make sure that all values in `TIMESTAMP`
are between two dates:

    agent_warn <- 
      create_agent(
          read_fn = ~tbl(con, in_schema("PUBLIC", "METERING_READINGS_TBL")),
          tbl_name = "METERING_READINGS_TBL",
          actions = action_levels(warn_at = 1000, stop_at = 200000)
        ) %>%
      col_is_character(vars(METERING_POINT_ID, PROPERTY, UNIT_OF_MEASURE)) %>% 
      col_is_numeric(vars(VALUE))%>%
      col_is_posix(vars(IMPORT_TIMESTAMP, TIMESTAMP)) %>% 
      col_vals_between(vars(TIMESTAMP), "2016-01-01", "2020-10-07 23:00:00") %>% 
      interrogate(extract_failed = FALSE)

    agent_warn

<!--html_preserve-->
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
@import url("https://unpkg.com/balloon-css/balloon.min.css");
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap");
html {
  font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', 'Fira Sans', 'Droid Sans', Arial, sans-serif;
}

#report .gt_table {
  display: table;
  border-collapse: collapse;
  margin-left: auto;
  margin-right: auto;
  color: #333333;
  font-size: 90%;
  font-weight: normal;
  font-style: normal;
  background-color: #FFFFFF;
  width: auto;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #A8A8A8;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #A8A8A8;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
}

#report .gt_heading {
  background-color: #FFFFFF;
  text-align: center;
  border-bottom-color: #FFFFFF;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#report .gt_title {
  color: #333333;
  font-size: 125%;
  font-weight: initial;
  padding-top: 4px;
  padding-bottom: 4px;
  border-bottom-color: #FFFFFF;
  border-bottom-width: 0;
}

#report .gt_subtitle {
  color: #333333;
  font-size: 85%;
  font-weight: initial;
  padding-top: 0;
  padding-bottom: 4px;
  border-top-color: #FFFFFF;
  border-top-width: 0;
}

#report .gt_bottom_border {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#report .gt_col_headings {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#report .gt_col_heading {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  overflow-x: hidden;
}

#report .gt_column_spanner_outer {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
}

#report .gt_column_spanner_outer:first-child {
  padding-left: 0;
}

#report .gt_column_spanner_outer:last-child {
  padding-right: 0;
}

#report .gt_column_spanner {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  overflow-x: hidden;
  display: inline-block;
  width: 100%;
}

#report .gt_group_heading {
  padding: 8px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
}

#report .gt_empty_group_heading {
  padding: 0.5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: middle;
}

#report .gt_from_md > :first-child {
  margin-top: 0;
}

#report .gt_from_md > :last-child {
  margin-bottom: 0;
}

#report .gt_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 10px;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  overflow-x: hidden;
}

#report .gt_stub {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 12px;
}

#report .gt_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#report .gt_first_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
}

#report .gt_grand_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#report .gt_first_grand_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: double;
  border-top-width: 6px;
  border-top-color: #D3D3D3;
}

#report .gt_striped {
  background-color: rgba(128, 128, 128, 0.05);
}

#report .gt_table_body {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#report .gt_footnotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#report .gt_footnote {
  margin: 0px;
  font-size: 90%;
  padding: 4px;
}

#report .gt_sourcenotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#report .gt_sourcenote {
  font-size: 90%;
  padding: 4px;
}

#report .gt_left {
  text-align: left;
}

#report .gt_center {
  text-align: center;
}

#report .gt_right {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

#report .gt_font_normal {
  font-weight: normal;
}

#report .gt_font_bold {
  font-weight: bold;
}

#report .gt_font_italic {
  font-style: italic;
}

#report .gt_super {
  font-size: 65%;
}

#report .gt_footnote_marks {
  font-style: italic;
  font-size: 65%;
}

#pb_information {
  -webkit-font-smoothing: antialiased;
}

#report .gt_row {
  overflow: visible;
}

#report .gt_sourcenote {
  height: 35px;
  padding: 0;
}

#report code {
  font-family: 'IBM Plex Mono', monospace, courier;
  font-size: 11px;
  background-color: transparent;
  padding: 0;
}
</style>
<div id="report" style="overflow-x:auto;overflow-y:auto;width:auto;height:auto;">
<table class="gt_table" style="table-layout: fixed;; width: 0px">
<colgroup>
<col style="width:6px;"/>
<col style="width:35px;"/>
<col style="width:190px;"/>
<col style="width:120px;"/>
<col style="width:120px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:50px;"/>
<col style="width:30px;"/>
<col style="width:30px;"/>
<col style="width:30px;"/>
<col style="width:65px;"/>
</colgroup>
<thead class="gt_header">
<tr>
<th colspan="14" class="gt_heading gt_title gt_font_normal" style="color: #444444; font-size: 28px; text-align: left; font-weight: 500;">
Pointblank Validation
</th>
</tr>
<tr>
<th colspan="14" class="gt_heading gt_subtitle gt_font_normal gt_bottom_border" style="font-size: 12px; text-align: left;">
<span
style="text-decoration-style:solid;text-decoration-color:#ADD8E6;text-decoration-line:underline;text-underline-position:under;color:#333333;font-variant-numeric:tabular-nums;padding-left:4px;margin-right:5px;padding-right:2px;">\[2020-12-04|16:02:14\]</span>
</p>

<span
style="background-color:#E2E2E2;color:#222222;padding:0.5em 0.5em;position:inherit;text-transform:uppercase;margin:5px 0px 5px 5px;font-weight:bold;border:solid 1px #E2E2E2;padding:2px 15px 2px 15px;font-size:smaller;"></span>
<span
style="background-color:none;color:#222222;padding:0.5em 0.5em;position:inherit;margin:5px 10px 5px -4px;font-weight:bold;border:solid 1px #E2E2E2;padding:2px 15px 2px 15px;font-size:smaller;">METERING\_READINGS\_TBL</span><span
style="background-color:#E5AB00;color:white;padding:0.5em 0.5em;position:inherit;text-transform:uppercase;margin:5px 0px 5px 5px;font-weight:bold;border:solid 1px #E5AB00;padding:2px 15px 2px 15px;font-size:smaller;">WARN</span>
<span
style="background-color:none;color:#333333;padding:0.5em 0.5em;position:inherit;margin:5px 0px 5px -4px;font-weight:bold;border:solid 1px #E5AB00;padding:2px 15px 2px 15px;font-size:smaller;">1,000</span>
<span
style="background-color:#D0182F;color:white;padding:0.5em 0.5em;position:inherit;text-transform:uppercase;margin:5px 0px 5px 1px;font-weight:bold;border:solid 1px #D0182F;padding:2px 15px 2px 15px;font-size:smaller;">STOP</span>
<span
style="background-color:none;color:#333333;padding:0.5em 0.5em;position:inherit;margin:5px 0px 5px -4px;font-weight:bold;border:solid 1px #D0182F;padding:2px 15px 2px 15px;font-size:smaller;">200,000</span>
<span
style="background-color:#499FFE;color:white;padding:0.5em 0.5em;position:inherit;text-transform:uppercase;margin:5px 0px 5px 1px;font-weight:bold;border:solid 1px #499FFE;padding:2px 15px 2px 15px;font-size:smaller;">NOTIFY</span>
<span
style="background-color:none;color:#333333;padding:0.5em 0.5em;position:inherit;margin:5px 0px 5px -4px;font-weight:bold;border:solid 1px #499FFE;padding:2px 15px 2px 15px;font-size:smaller;">—</span>

</th>
</tr>
</thead>
<thead class="gt_col_headings">
<tr>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
STEP
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
COLUMNS
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
VALUES
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
TBL
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
EVAL
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
⋅ ⋅ ⋅
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
PASS
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
FAIL
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
W
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
S
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
N
</th>
<th class="gt_col_heading gt_columns_bottom_border gt_center" rowspan="1" colspan="1" style="color: #666666; font-weight: bold;">
EXT
</th>
</tr>
</thead>
<tbody class="gt_table_body">
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
1
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_character" transform="translate(-0.397206, 0.151308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="c" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="39.9695669" y="43.0146694">c</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_character()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>METERING\_POINT\_ID</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
2
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_character" transform="translate(-0.397206, 0.151308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="c" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="39.9695669" y="43.0146694">c</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_character()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>PROPERTY</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
3
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_character" transform="translate(-0.397206, 0.151308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="c" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="39.9695669" y="43.0146694">c</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_character()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>UNIT\_OF\_MEASURE</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
4
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs></defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_numeric" transform="translate(-0.397206, 0.359210)">
<path d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z" id="rectangle" stroke="#000000" stroke-width="2"></path>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="d" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="38.4461294" y="43.0146694">d</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_numeric()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>VALUE</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
5
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_posix" transform="translate(-0.397206, 0.785474)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="T" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="38.4080435" y="43.0146694">T</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_posix()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>IMPORT\_TIMESTAMP</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #4CA64C; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
6
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0.014669353 L56.712234,0.014669353 C62.2350815,0.014669353 66.712234,4.49182185 66.712234,10.0146694 L66.712234,66.0146694 L10.712234,66.0146694 C5.18938647,66.0146694 0.712233968,61.5375169 0.712233968,56.0146694 L0.712233968,10.0146694 C0.712233968,4.49182185 5.18938647,0.014669353 10.712234,0.014669353 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_is_posix" transform="translate(-0.397206, 0.785474)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65.0146694 L65.712234,10.0146694 C65.712234,5.0441066 61.6827967,1.01466935 56.712234,1.01466935 L10.712234,1.01466935 C5.74167122,1.01466935 1.71223397,5.0441066 1.71223397,10.0146694 L1.71223397,56.0146694 C1.71223397,60.9852321 5.74167122,65.0146694 10.712234,65.0146694 L65.712234,65.0146694 Z"></path>
</g>
<rect id="column" fill="#000000" x="12.2117153" y="12.0146694" width="20" height="42" rx="1"></rect>
<text id="T" font-family="LucidaGrande, Lucida Grande" font-size="26" font-weight="normal" fill="#000000">
<tspan x="38.4080435" y="43.0146694">T</tspan> </text> </g> </g>
</svg>

<code style="font-size:11px;"> col\_is\_posix()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>TIMESTAMP</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
—
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>1</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>1</code><br><code>1.00</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>0</code><br><code>0.00</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
<tr>
<td class="gt_row gt_left" style="background-color: #FFBF00; height:  40px">
</td>
<td class="gt_row gt_right" style="color: #666666; font-size: 13px; font-weight: bold; height:  40px">
7
</td>
<td class="gt_row gt_left" style="height:  40px">

<svg width="30px" height="30px" viewBox="0 0 67 67" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<path d="M10.712234,0 L56.712234,0 C62.2350815,-1.01453063e-15 66.712234,4.4771525 66.712234,10 L66.712234,66 L10.712234,66 C5.18938647,66 0.712233968,61.5228475 0.712233968,56 L0.712233968,10 C0.712233968,4.4771525 5.18938647,1.01453063e-15 10.712234,0 Z" id="path-1"></path>
</defs>
<g id="pointblank" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
<g id="col_vals_between" transform="translate(-0.487938, 0.651308)">
<g id="rectangle">
<use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
<path stroke="#000000" stroke-width="2" d="M65.712234,65 L65.712234,10 C65.712234,5.02943725 61.6827967,1 56.712234,1 L10.712234,1 C5.74167122,1 1.71223397,5.02943725 1.71223397,10 L1.71223397,56 C1.71223397,60.9705627 5.74167122,65 10.712234,65 L65.712234,65 Z"></path>
</g>
<path d="M11.993484,21.96875 C10.962234,22.082031 10.188797,22.964844 10.212234,24 L10.212234,42 C10.200515,42.722656 10.579422,43.390625 11.204422,43.753906 C11.825515,44.121094 12.598953,44.121094 13.220047,43.753906 C13.845047,43.390625 14.223953,42.722656 14.212234,42 L14.212234,24 C14.220047,23.457031 14.009109,22.9375 13.626297,22.554688 C13.243484,22.171875 12.723953,21.960938 12.180984,21.96875 C12.118484,21.964844 12.055984,21.964844 11.993484,21.96875 Z M55.993484,21.96875 C54.962234,22.082031 54.188797,22.964844 54.212234,24 L54.212234,42 C54.200515,42.722656 54.579422,43.390625 55.204422,43.753906 C55.825515,44.121094 56.598953,44.121094 57.220047,43.753906 C57.845047,43.390625 58.223953,42.722656 58.212234,42 L58.212234,24 C58.220047,23.457031 58.009109,22.9375 57.626297,22.554688 C57.243484,22.171875 56.723953,21.960938 56.180984,21.96875 C56.118484,21.964844 56.055984,21.964844 55.993484,21.96875 Z M16.212234,22 C15.661453,22 15.212234,22.449219 15.212234,23 C15.212234,23.550781 15.661453,24 16.212234,24 C16.763015,24 17.212234,23.550781 17.212234,23 C17.212234,22.449219 16.763015,22 16.212234,22 Z M20.212234,22 C19.661453,22 19.212234,22.449219 19.212234,23 C19.212234,23.550781 19.661453,24 20.212234,24 C20.763015,24 21.212234,23.550781 21.212234,23 C21.212234,22.449219 20.763015,22 20.212234,22 Z M24.212234,22 C23.661453,22 23.212234,22.449219 23.212234,23 C23.212234,23.550781 23.661453,24 24.212234,24 C24.763015,24 25.212234,23.550781 25.212234,23 C25.212234,22.449219 24.763015,22 24.212234,22 Z M28.212234,22 C27.661453,22 27.212234,22.449219 27.212234,23 C27.212234,23.550781 27.661453,24 28.212234,24 C28.763015,24 29.212234,23.550781 29.212234,23 C29.212234,22.449219 28.763015,22 28.212234,22 Z M32.212234,22 C31.661453,22 31.212234,22.449219 31.212234,23 C31.212234,23.550781 31.661453,24 32.212234,24 C32.763015,24 33.212234,23.550781 33.212234,23 C33.212234,22.449219 32.763015,22 32.212234,22 Z M36.212234,22 C35.661453,22 35.212234,22.449219 35.212234,23 C35.212234,23.550781 35.661453,24 36.212234,24 C36.763015,24 37.212234,23.550781 37.212234,23 C37.212234,22.449219 36.763015,22 36.212234,22 Z M40.212234,22 C39.661453,22 39.212234,22.449219 39.212234,23 C39.212234,23.550781 39.661453,24 40.212234,24 C40.763015,24 41.212234,23.550781 41.212234,23 C41.212234,22.449219 40.763015,22 40.212234,22 Z M44.212234,22 C43.661453,22 43.212234,22.449219 43.212234,23 C43.212234,23.550781 43.661453,24 44.212234,24 C44.763015,24 45.212234,23.550781 45.212234,23 C45.212234,22.449219 44.763015,22 44.212234,22 Z M48.212234,22 C47.661453,22 47.212234,22.449219 47.212234,23 C47.212234,23.550781 47.661453,24 48.212234,24 C48.763015,24 49.212234,23.550781 49.212234,23 C49.212234,22.449219 48.763015,22 48.212234,22 Z M52.212234,22 C51.661453,22 51.212234,22.449219 51.212234,23 C51.212234,23.550781 51.661453,24 52.212234,24 C52.763015,24 53.212234,23.550781 53.212234,23 C53.212234,22.449219 52.763015,22 52.212234,22 Z M21.462234,27.96875 C21.419265,27.976563 21.376297,27.988281 21.337234,28 C21.177078,28.027344 21.02864,28.089844 20.899734,28.1875 L15.618484,32.1875 C15.356765,32.375 15.200515,32.679688 15.200515,33 C15.200515,33.320313 15.356765,33.625 15.618484,33.8125 L20.899734,37.8125 C21.348953,38.148438 21.985672,38.058594 22.321609,37.609375 C22.657547,37.160156 22.567703,36.523438 22.118484,36.1875 L19.212234,34 L49.212234,34 L46.305984,36.1875 C45.856765,36.523438 45.766922,37.160156 46.102859,37.609375 C46.438797,38.058594 47.075515,38.148438 47.524734,37.8125 L52.805984,33.8125 C53.067703,33.625 53.223953,33.320313 53.223953,33 C53.223953,32.679688 53.067703,32.375 52.805984,32.1875 L47.524734,28.1875 C47.30989,28.027344 47.040359,27.960938 46.774734,28 C46.743484,28 46.712234,28 46.680984,28 C46.282547,28.074219 45.96614,28.382813 45.884109,28.78125 C45.802078,29.179688 45.970047,29.585938 46.305984,29.8125 L49.212234,32 L19.212234,32 L22.118484,29.8125 C22.520828,29.566406 22.696609,29.070313 22.536453,28.625 C22.380203,28.179688 21.930984,27.90625 21.462234,27.96875 Z M16.212234,42 C15.661453,42 15.212234,42.449219 15.212234,43 C15.212234,43.550781 15.661453,44 16.212234,44 C16.763015,44 17.212234,43.550781 17.212234,43 C17.212234,42.449219 16.763015,42 16.212234,42 Z M20.212234,42 C19.661453,42 19.212234,42.449219 19.212234,43 C19.212234,43.550781 19.661453,44 20.212234,44 C20.763015,44 21.212234,43.550781 21.212234,43 C21.212234,42.449219 20.763015,42 20.212234,42 Z M24.212234,42 C23.661453,42 23.212234,42.449219 23.212234,43 C23.212234,43.550781 23.661453,44 24.212234,44 C24.763015,44 25.212234,43.550781 25.212234,43 C25.212234,42.449219 24.763015,42 24.212234,42 Z M28.212234,42 C27.661453,42 27.212234,42.449219 27.212234,43 C27.212234,43.550781 27.661453,44 28.212234,44 C28.763015,44 29.212234,43.550781 29.212234,43 C29.212234,42.449219 28.763015,42 28.212234,42 Z M32.212234,42 C31.661453,42 31.212234,42.449219 31.212234,43 C31.212234,43.550781 31.661453,44 32.212234,44 C32.763015,44 33.212234,43.550781 33.212234,43 C33.212234,42.449219 32.763015,42 32.212234,42 Z M36.212234,42 C35.661453,42 35.212234,42.449219 35.212234,43 C35.212234,43.550781 35.661453,44 36.212234,44 C36.763015,44 37.212234,43.550781 37.212234,43 C37.212234,42.449219 36.763015,42 36.212234,42 Z M40.212234,42 C39.661453,42 39.212234,42.449219 39.212234,43 C39.212234,43.550781 39.661453,44 40.212234,44 C40.763015,44 41.212234,43.550781 41.212234,43 C41.212234,42.449219 40.763015,42 40.212234,42 Z M44.212234,42 C43.661453,42 43.212234,42.449219 43.212234,43 C43.212234,43.550781 43.661453,44 44.212234,44 C44.763015,44 45.212234,43.550781 45.212234,43 C45.212234,42.449219 44.763015,42 44.212234,42 Z M48.212234,42 C47.661453,42 47.212234,42.449219 47.212234,43 C47.212234,43.550781 47.661453,44 48.212234,44 C48.763015,44 49.212234,43.550781 49.212234,43 C49.212234,42.449219 48.763015,42 48.212234,42 Z M52.212234,42 C51.661453,42 51.212234,42.449219 51.212234,43 C51.212234,43.550781 51.661453,44 52.212234,44 C52.763015,44 53.212234,43.550781 53.212234,43 C53.212234,42.449219 52.763015,42 52.212234,42 Z" id="inside_range" fill="#000000" fill-rule="nonzero"></path>
</g> </g>
</svg>

<code style="font-size:11px;"> col\_vals\_between()</code>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<p style="margin-top:0;margin-bottom:0;font-size:11px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;line-height:2em;">
<code><span style="color:purple;">▮</span>TIMESTAMP</code>
</p>

</td>
<td class="gt_row gt_left" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">

<div aria-label="[2016-01-01, 2020-10-07 23:00:00]" data-balloon-pos="left"><p style="margin-top: 0px; margin-bottom: 0px; font-size: 11px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;"><code>[2016-01-01, 2020-10-07 23:00:00]</code></p></div>

</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:0;color:#333333;vertical-align:middle;font-size:18px;border:none;border-radius:4px;"
aria-label="No modifications of the table."
data-balloon-pos="left">→</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span
style="background:transparent;padding:5px;color:#4CA64C;vertical-align:middle;font-size:15px;border:none;"
aria-label="No evaluation issues." data-balloon-pos="left">✓</span>
</p>

</td>
<td class="gt_row gt_right" style="height:  40px">
<code>691M</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>691M</code><br><code>0.99</code>
</td>
<td class="gt_row gt_right" style="border-left-width: 1px; border-left-style: dashed; border-left-color: #E5E5E5; height:  40px">
<code>183K</code><br><code>0.01</code>
</td>
<td class="gt_row gt_center" style="border-left-width: 1px; border-left-style: solid; border-left-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #E5AB00;">●</span>
</p>

</td>
<td class="gt_row gt_center" style="background-color: #FCFCFC; height:  40px">

<p>
<span style="color: #CF142B;">○</span>
</p>

</td>
<td class="gt_row gt_center" style="border-right-width: 1px; border-right-style: solid; border-right-color: #D3D3D3; background-color: #FCFCFC; height:  40px">

<p>
—
</p>

</td>
<td class="gt_row gt_center" style="height:  40px">

<p>
—
</p>

</td>
</tr>
</tbody>
<tfoot class="gt_sourcenotes">
<tr>
<td class="gt_sourcenote" colspan="14">
<span
style="background-color: #FFF;color: #444;padding: 0.5em 0.5em;position: inherit;text-transform: uppercase;margin-left: 10px;border: solid 1px #999999;font-variant-numeric: tabular-nums;border-radius: 0;padding: 2px 10px 2px 10px;font-size: smaller;">2020-12-04
16:02:20 CET</span><span
style="background-color: #FFF;color: #444;padding: 0.5em 0.5em;position: inherit;margin: 5px 1px 5px 0;border: solid 1px #999999;border-left: none;font-variant-numeric: tabular-nums;border-radius: 0;padding: 2px 10px 2px 10px;font-size: smaller;">4.2
s</span><span
style="background-color: #FFF;color: #444;padding: 0.5em 0.5em;position: inherit;text-transform: uppercase;margin: 5px 1px 5px -1px;border: solid 1px #999999;border-left: none;border-radius: 0;padding: 2px 10px 2px 10px;font-size: smaller;">2020-12-04
16:02:24 CET</span>
</td>
</tr>
</tfoot>
</table>
</div>
<!--/html_preserve-->

As you can see we have 183K observations that are not in the date range which will only cause a warning. 

Creating notification emails
----------------------------

Many data validation tasks, at least for a Data Scientist, look
something like this: you want to check that the data behaves as you
expect, and if not you would like to get some kind of notification.
`pointblank` has great functionality for this and makes it easy to write
data validation reports that may be sent out by email through the
[`blastula`](https://github.com/rstudio/blastula) package, which is also created by *Rich Iannone*.

To create a skeleton for an email we just use `email_create()` on the
agent.

Below I create a simple function that simply sends an email if the not
all steps are passed.

    library(blastula)
    
    send_validation_email <- function(agent){
      
      if(!isTRUE(all_passed(agent))){
        
        email_agent <- email_create(agent)  
        
        table_name <- agent$tbl_name
        
        subject <- glue::glue("There was at least a warning in the data validation of {table_name}")
        
        email_agent %>%
          smtp_send(
            to = "filip.wastberg@solita.fi", 
            from = "filip.wastberg@solita.fi",
            subject = subject,
            credentials = creds_key(id = "outlook")
          )
      } else {
        message("Everything passed, no need to send email.")
      }
    }

    send_validation_email(agent_warn)

Which, if there are any warnings, result in this mail:

![](/img/data-quality-r/pointblank-mail.png)

Of course, this is a simple example and can be further developed. This
can also be configured to be run with Docker or a Data Science platform
such as [`RStudio Connect`](https://rstudio.com/products/connect/),
which would be a recommendation if something like this is to be run in
“production”.

And it doesn’t end here. `pointblank` can generate `YAML`-files for you
and the validation functions are really flexible if your needs are more
specific.

Summary
-------

R is often regarded as a niche programming language. And there is no
reason to sugar code it, R is a weird language. But today it is one of
the [top ten most popular programming
languages](https://www.tiobe.com/tiobe-index/) (not bad for a niche
language), it has over 15 000 open source libraries and is used for
everything from building machine learning models to advanced web
applications and, as we have showed here, data validation. Furthermore,
the development of R the last few years have had a lot of focus on
syntax and making it easy to use, an often overlooked part of
programming development, and this, I think, is one reason it continues
to attract more users. `pointblank` is one of those packages who takes a
complex task and gives it a nice API through what is basically a domain
specific language. Making R even more user friendly.

And last but not least, it is pretty. And we love pretty things.