-- Ensure the base Builder profile exists before extending it. This keeps the
-- migration safe when the base schema was not applied in the target project.
CREATE TABLE IF NOT EXISTS public.builder_profiles (
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

ALTER TABLE public.builder_profiles
    ADD COLUMN IF NOT EXISTS gst_number text DEFAULT '',
    ADD COLUMN IF NOT EXISTS portfolio_summary text DEFAULT '',
    ADD COLUMN IF NOT EXISTS website text DEFAULT '',
    ADD COLUMN IF NOT EXISTS specializations text DEFAULT '';

CREATE TABLE IF NOT EXISTS public.builder_projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    project_name text NOT NULL,
    estimated_value text DEFAULT '',
    description text DEFAULT '',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.builder_quotations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    customer_name text NOT NULL DEFAULT '',
    project_name text NOT NULL DEFAULT '',
    amount text DEFAULT '',
    status text NOT NULL DEFAULT 'Draft' CHECK (status IN ('Draft', 'Sent', 'Accepted', 'Rejected')),
    notes text DEFAULT '',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS builder_projects_user_id_idx ON public.builder_projects(user_id);
CREATE INDEX IF NOT EXISTS builder_quotations_user_id_idx ON public.builder_quotations(user_id);

NOTIFY pgrst, 'reload schema';