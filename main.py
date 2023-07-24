# Importing libs
import pandas as pd
import matplotlib.pyplot as plt

# ... YOUR CODE FOR TASK 1 ...

# Loading in the data
pulls_one = pd.read_csv('datasets/pulls_2011-2013.csv')
pulls_two = pd.read_csv('datasets/pulls_2014-2018.csv')
pull_files = pd.read_csv('datasets/pull_files.csv')

print("pulls_one: ", pulls_one)
print("pulls_two: ", pulls_two)
print("pull_files: ", pull_files)

# Append pulls_one to pulls_two
pulls = pulls_one._append(pulls_two, ignore_index=True)

print("appended pulls_one/two: ", pulls)

# Convert the date for the pulls object
pulls['date'] = pd.to_datetime(pulls['date'], utc=True)

print("converted date for the pulls object: ", pulls['date'])

# Merge the two DataFrames
data = pulls.merge(pull_files, on='pid')

print('merged pulls and pull_files: ', data)

# Create a column that will store the month
data['month'] = data['date'].dt.month

print('column to store month: ', data['month'])

# # Create a column that will store the year
data['year'] = data['date'].dt.year

print('column to store year: ', data['year'])

# Group by the month and year and count the pull requests
counts = data.groupby(['month', 'year'])['pid'].count()

print('pull requests group by month and year: ', counts)

# Plot the results
counts.plot(kind='bar', figsize=(12, 4))

# Add title and labels
plt.title("Bar Plot of Counts")
plt.xlabel("Categories")
plt.ylabel("Counts")

# Display the plot
plt.show()

# # Group by the submitter
by_user = data.groupby('user').agg({'pid': 'count'})

print('group by submitter: ', by_user)

# # Plot the histogram
# # ... YOUR CODE FOR TASK 5 ...
by_user.hist()
plt.show()

# # Identify the last 10 pull requests
last_10 = pulls.sort_values(by = 'date').tail(10)
print('last_10: ', last_10)

# # Join the two data sets
joined_pr = last_10.merge(pull_files, on='pid')
print('joined_pr: ', joined_pr)

# # Identify the unique files
files = set(joined_pr['file'])

# # Print the results
print('files: ', files)

# # This is the file we are interested in:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# # Identify the commits that changed the file
file_pr = data[data['file'] == file]
print('file_pr: ', file_pr)

# # Count the number of changes made by each developer
author_counts = file_pr.groupby('user').count()
print('author_counts: ', author_counts)

# # Print the top 3 developers
# # ... YOUR CODE FOR TASK 7 ...
author_counts.nlargest(3, 'file')
print('top 3 dev: ', author_counts.nlargest(3, 'file'))

file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# # Select the pull requests that changed the target file
file_pr = pull_files[pull_files['file'] == file]
print('file_pr: ', file_pr)

# # Merge the obtained results with the pulls DataFrame
joined_pr = pulls.merge(file_pr, on='pid')
print('joined_pr: ', joined_pr)

# # Find the users of the last 10 most recent pull requests
users_last_10 = set(joined_pr.nlargest(10, 'date')['user'])

# # Printing the results
print('users_last_10: ', users_last_10)

# # The developers we are interested in
authors = ['xeno-by', 'soc']
print('authors: ', authors)

# # Get all the developers' pull requests
by_author = pulls[pulls['user'].isin(authors)]
print('by_author: ', by_author)

# # Count the number of pull requests submitted each year
counts = by_author.groupby([by_author['user'], by_author['date'].dt.year]).agg({'pid': 'count'}).reset_index()
print('counts: ', counts)

# # Convert the table to a wide format
counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)
print('counts_wide: ', counts_wide)

# # Plot the results
# # ... YOUR CODE FOR TASK 9 ...
counts_wide.plot(kind='bar')
plt.show()

authors = ['xeno-by', 'soc']
print('authors: ', authors)

file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Merge DataFrames and select the pull requests by the author
by_author = data[data['user'].isin(authors)]
print('by_author: ', by_author)

# Select the pull requests that affect the file
by_file = by_author[by_author['file'] == file]
print('by_file: ', by_file)

# Group and count the number of PRs done by each user each year
grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()
print('grouped: ', grouped)

# Transform the data into a wide format
by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)
print('by_file_wide: ', by_file_wide)

# Plot the results
by_file_wide.plot(kind='bar')
plt.show()