
Part 2
~~~~~

Now, as you move to v2 of your gift registry, you don't want to lose the
1000 users you already have and their history of buying gifts for each other.
How will you handle this? If you're familiar with any 3rd-party tools to
handle this transition, please use them to write out a solution. If not, you
can write out a script or some SQL to describe what needs to happen to
transition from v1 to v2. Could you implement the transition with no downtime?

There are a few 3rd party tools I used before for DB schema migration
 - "SQLAlchemy Migrate Tool" and
 - "Alembic"

In the v2 I would do migration from v1 in 3-4 steps:

  1. Create `contribution` table 
  2. Create records in the `contribution` table based on 
     `gift.bought_by`, `gift.bought_date` and `gift.price` data
  3. Drop `gift.bought_by` column
  4. Update value of `gift.contrib_sum`
