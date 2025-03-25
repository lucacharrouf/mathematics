CREATE TABLE IF NOT EXISTS waitlist (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

DROP POLICY IF EXISTS "Allow public read access" ON waitlist;
DROP POLICY IF EXISTS "Allow public insert access" ON waitlist;

CREATE POLICY "Allow public read access"
ON waitlist FOR SELECT
USING (true);

CREATE POLICY "Allow public insert access"
ON waitlist FOR INSERT
WITH CHECK (true);

ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

alter publication supabase_realtime add table waitlist;