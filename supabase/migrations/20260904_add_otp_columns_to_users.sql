ALTER TABLE public.users
    ADD COLUMN IF NOT EXISTS otp_salt text,
    ADD COLUMN IF NOT EXISTS otp_hash text,
    ADD COLUMN IF NOT EXISTS otp_expires_at timestamptz,
    ADD COLUMN IF NOT EXISTS otp_attempts integer NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS otp_invalidated boolean NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS otp_last_sent_at timestamptz,
    ADD COLUMN IF NOT EXISTS otp_delivery_status boolean NOT NULL DEFAULT false;

-- Refresh PostgREST schema cache so the new OTP columns are visible to the app.
NOTIFY pgrst, 'reload schema';
