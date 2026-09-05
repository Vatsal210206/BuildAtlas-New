-- Repair migration for deployments where the profile tables were never
-- created or were not visible to PostgREST.
CREATE TABLE IF NOT EXISTS public.vendor_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    business_name text NOT NULL,
    contact_name text NOT NULL,
    phone text NOT NULL,
    address text DEFAULT '',
    city text DEFAULT '',
    state text DEFAULT '',
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.builder_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    business_name text NOT NULL,
    contact_name text NOT NULL,
    phone text NOT NULL,
    address text DEFAULT '',
    city text DEFAULT '',
    state text DEFAULT '',
    gst_number text DEFAULT '',
    portfolio_summary text DEFAULT '',
    website text DEFAULT '',
    specializations text DEFAULT '',
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.customer_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    full_name text NOT NULL,
    phone text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE public.builder_profiles
    ADD COLUMN IF NOT EXISTS gst_number text DEFAULT '',
    ADD COLUMN IF NOT EXISTS portfolio_summary text DEFAULT '',
    ADD COLUMN IF NOT EXISTS website text DEFAULT '',
    ADD COLUMN IF NOT EXISTS specializations text DEFAULT '';

NOTIFY pgrst, 'reload schema';