# Business Scenario

**Company:** SocialPulse Analytics Pvt. Ltd.

The company wants to understand how social media usage affects users' mental health, sleep quality, productivity, and addiction levels. Management needs an interactive Excel dashboard to identify high-risk users and behavioral trends.

---

# Dashboard KPI Cards

Create KPI cards using Pivot Tables.

* Total Users
* Average Daily Usage Hours
* Average Mental Wellbeing Score
* Average Anxiety Score
* Average Productivity Loss
* Average Sleep Hours
* Severe Addiction Users
* High Addiction Users
* Average Notifications per Day

---

# Business Question 1

## Which social media platform has the highest addiction level?

### Pivot Table

Rows

```
Primary_Platform
```

Columns

```
Addiction_Level
```

Values

```
Count of User_ID
```

Chart

* Stacked Column Chart

Business Insight

> Which platform contributes the largest number of severe addiction users?

---

# Business Question 2

## Which occupation spends the most time on social media?

Rows

```
Occupation
```

Values

```
Average of Daily_Usage_Hours
```

Chart

* Bar Chart

Business Decision

Should awareness campaigns target students or working professionals?

---

# Business Question 3

## Does higher daily usage increase anxiety?

Rows

```
Daily Usage Group
```

(Create groups in Pivot)

Values

```
Average Anxiety Score
```

Chart

* Line Chart

---

# Business Question 4

## Which age group is most addicted?

Create Age Groups

```
18-24
25-34
35-44
45+
```

Rows

```
Age Group
```

Columns

```
Addiction_Level
```

Values

```
Count of User_ID
```

Chart

100% Stacked Column

---

# Business Question 5

## Which platform causes the greatest productivity loss?

Rows

```
Primary_Platform
```

Values

```
Average Productivity_Loss_Score
```

Chart

Clustered Bar

---

# Business Question 6

## Which relationship status has the highest loneliness?

Rows

```
Relationship_Status
```

Values

```
Average Loneliness Score
```

Chart

Column Chart

---

# Business Question 7

## Does late-night usage reduce sleep quality?

Rows

```
Late_Night_Usage
```

Values

```
Average Sleep Quality Score
Average Sleep Hours
```

Chart

Combo Chart

---

# Business Question 8

## Which platform generates the highest number of notifications?

Rows

```
Primary_Platform
```

Values

```
Average Notifications per Day
```

Chart

Column Chart

---

# Business Question 9

## How many users tried to reduce social media usage?

Rows

```
Tried_To_Cut_Back
```

Values

```
Count of User_ID
```

Chart

Pie Chart

---

# Business Question 10

## How many users failed after trying to reduce usage?

Rows

```
Failed_To_Cut_Back
```

Values

```
Count of User_ID
```

Filters

```
Tried_To_Cut_Back = Yes
```

Chart

Column Chart

---

# Business Question 11

## Which occupation has the highest FOMO?

Rows

```
Occupation
```

Values

```
Average FOMO Score
```

Chart

Bar Chart

---

# Business Question 12

## Which gender experiences the highest social comparison?

Rows

```
Gender
```

Values

```
Average Social Comparison Score
```

Chart

Column Chart

---

# Business Question 13

## How does screen-free time impact mental wellbeing?

Rows

```
Screen_Free_Time_Hrs
```

(Group into bins)

Values

```
Average Mental Wellbeing Score
```

Chart

Line Chart

---

# Business Question 14

## Which addiction level has the poorest sleep quality?

Rows

```
Addiction_Level
```

Values

```
Average Sleep Quality Score
```

Chart

Column Chart

---

# Business Question 15

## Which platform has users with the highest depression score?

Rows

```
Primary_Platform
```

Values

```
Average Depression Score
```

Chart

Bar Chart

---

# Business Question 16

## Does physical activity improve mental wellbeing?

Rows

```
Physical Activity Group
```

(Create groups)

Values

```
Average Mental Wellbeing Score
```

Chart

Line Chart

---

# Business Question 17

## Morning phone checking behavior by addiction level

Rows

```
First_Check_Morning
```

Columns

```
Addiction_Level
```

Values

```
Count of User_ID
```

Chart

Stacked Bar

---

# Business Question 18

## Which platform is most popular?

Rows

```
Primary_Platform
```

Values

```
Count of User_ID
```

Chart

Pie Chart

---

# Business Question 19

## Which occupation has the highest validation-seeking behavior?

Rows

```
Occupation
```

Values

```
Average Validation Seeking Score
```

Chart

Column Chart

---

# Business Question 20

## Which users have the highest productivity loss?

Rows

```
Addiction_Level
```

Values

```
Average Productivity Loss Score
```

Chart

Column Chart

---

# Business Question 21

## Does social comparison increase depression?

Rows

```
Social Comparison Group
```

Values

```
Average Depression Score
```

Chart

Scatter Plot (or grouped line chart after binning)

---

# Business Question 22

## Which age group sleeps the least?

Rows

```
Age Group
```

Values

```
Average Sleep Hours
```

Chart

Bar Chart

---

# Business Question 23

## Which platform has users with the best mental wellbeing?

Rows

```
Primary_Platform
```

Values

```
Average Mental Wellbeing Score
```

Chart

Column Chart

---

# Business Question 24

## Does excessive scrolling increase loneliness?

Rows

```
Scroll Without Purpose Group
```

Values

```
Average Loneliness Score
```

Chart

Line Chart

---

# Business Question 25

## Which occupation suffers the greatest productivity loss?

Rows

```
Occupation
```

Values

```
Average Productivity Loss Score
```

Chart

Horizontal Bar

---

# Recommended Dashboard Layout

```
-------------------------------------------------------
                    SOCIAL MEDIA DASHBOARD
-------------------------------------------------------

[KPI]
Users | Avg Usage | Avg Anxiety | Avg Sleep | Avg Wellbeing

-------------------------------------------------------
Platform Analysis
-----------------
Platform vs Addiction
Platform vs Productivity
Platform Popularity

-------------------------------------------------------
Mental Health
-------------
Anxiety by Age
Depression by Platform
Loneliness by Relationship
Sleep Quality by Addiction

-------------------------------------------------------
Behavior Analysis
-----------------
Notifications
Late Night Usage
Morning Check
Tried to Cut Back
Failed to Cut Back

-------------------------------------------------------
Demographics
-------------
Gender
Occupation
Relationship Status
Age Group

-------------------------------------------------------
Slicers

✓ Gender
✓ Occupation
✓ Platform
✓ Addiction Level
✓ Relationship Status
✓ Age Group

Timeline (if date fields are added)
```

This set of questions is suitable for a **beginner-to-intermediate Excel dashboard project**, covering **Pivot Tables, Pivot Charts, Slicers, KPI Cards, Conditional Formatting, and Dashboard Design** while reflecting realistic business analytics tasks.
