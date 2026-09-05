create table if not exists vendor_order_unlocks (
    id uuid primary key default gen_random_uuid(),
    order_id uuid not null references orders(id) on delete cascade,
    vendor_id uuid not null references users(id) on delete cascade,
    fee_amount_paise integer not null check (fee_amount_paise = 4900),
    currency text not null default 'INR' check (currency = 'INR'),
    razorpay_order_id text not null unique,
    razorpay_payment_id text unique,
    payment_status text not null default 'created' check (payment_status in ('created','paid','failed')),
    unlocked boolean not null default false,
    payment_timestamp timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(vendor_id, order_id)
);

create index if not exists vendor_order_unlocks_vendor_order_idx
    on vendor_order_unlocks(vendor_id, order_id);