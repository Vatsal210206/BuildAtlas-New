create extension if not exists pgcrypto;

create table if not exists users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    phone text not null unique,
    password_hash text not null,
    password_salt text not null,
    role text not null check (role in ('CUSTOMER', 'BUILDER / CONTRACTOR', 'DEALER / SUPPLIER', 'ADMIN')),
    verified boolean not null default false,
    otp_salt text,
    otp_hash text,
    otp_expires_at timestamptz,
    otp_attempts integer not null default 0,
    otp_invalidated boolean not null default false,
    otp_last_sent_at timestamptz,
    otp_delivery_status boolean not null default false,
    created_at timestamptz not null default now()
);

create table if not exists vendor_profiles (
    id uuid primary key default gen_random_uuid(), user_id uuid not null unique references users(id) on delete cascade,
    business_name text not null, contact_name text not null, phone text not null, address text default '', city text default '', state text default '', created_at timestamptz not null default now()
);
create table if not exists builder_profiles (
    id uuid primary key default gen_random_uuid(), user_id uuid not null unique references users(id) on delete cascade,
    business_name text not null, contact_name text not null, phone text not null, address text default '', city text default '', state text default '',
    gst_number text default '', portfolio_summary text default '', website text default '', specializations text default '', created_at timestamptz not null default now()
);
create table if not exists builder_projects (
    id uuid primary key default gen_random_uuid(), user_id uuid not null references users(id) on delete cascade,
    project_name text not null, city text default '', status text not null default 'Planning', progress integer not null default 0 check (progress between 0 and 100),
    estimated_value text default '', description text default '', created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists builder_quotations (
    id uuid primary key default gen_random_uuid(), user_id uuid not null references users(id) on delete cascade,
    customer_name text not null default '', project_name text not null default '', amount text default '', status text not null default 'Draft' check (status in ('Draft','Sent','Accepted','Rejected')),
    notes text default '', created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists customer_profiles (
    id uuid primary key default gen_random_uuid(), user_id uuid not null unique references users(id) on delete cascade,
    full_name text not null, phone text not null, created_at timestamptz not null default now()
);
create table if not exists products (
    id uuid primary key default gen_random_uuid(), vendor_id uuid not null references users(id) on delete cascade,
    product_name text not null, category text not null, brand text not null, price numeric(14,2) not null check (price >= 0), unit text not null,
    stock_quantity integer not null default 0 check (stock_quantity >= 0), low_stock_threshold integer not null default 500 check (low_stock_threshold >= 0), delivery_time integer not null default 0 check (delivery_time >= 0), created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists enquiries (
    id uuid primary key default gen_random_uuid(), buyer_id uuid not null references users(id) on delete cascade, vendor_id uuid not null references users(id) on delete cascade, product_id uuid not null references products(id) on delete restrict,
    quantity numeric(14,2) not null check (quantity > 0), location text default '', message text default '', status text not null default 'New' check (status in ('New','Responded','Awaiting Details','Closed')), created_at timestamptz not null default now()
);
create table if not exists quotations (
    id uuid primary key default gen_random_uuid(), enquiry_id uuid not null unique references enquiries(id) on delete cascade, vendor_id uuid not null references users(id) on delete cascade, buyer_id uuid not null references users(id) on delete cascade, product_id uuid not null references products(id) on delete restrict,
    quantity numeric(14,2) not null check (quantity > 0), unit_price numeric(14,2) not null check (unit_price >= 0), delivery_charge numeric(14,2) not null default 0 check (delivery_charge >= 0), total_amount numeric(14,2) not null check (total_amount >= 0), estimated_delivery integer not null default 0, status text not null default 'Draft' check (status in ('Draft','Sent','Accepted','Rejected','Expired')), created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists orders (
    id uuid primary key default gen_random_uuid(), quotation_id uuid not null unique references quotations(id) on delete restrict, buyer_id uuid not null references users(id) on delete cascade, vendor_id uuid not null references users(id) on delete cascade, total_amount numeric(14,2) not null check (total_amount >= 0), delivery_location text default '', status text not null default 'New' check (status in ('New','Confirmed','Processing','Ready for Dispatch','Dispatched','Delivered','Cancelled')), created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists deliveries (
    id uuid primary key default gen_random_uuid(), order_id uuid not null unique references orders(id) on delete cascade, status text not null default 'Not Scheduled' check (status in ('Not Scheduled','Scheduled','Dispatched','Delivered')), dispatch_date date, expected_delivery_date date, vehicle_number text default '', driver_name text default '', created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists reviews (
    id uuid primary key default gen_random_uuid(), order_id uuid not null references orders(id) on delete cascade, reviewer_id uuid not null references users(id) on delete cascade, vendor_id uuid not null references users(id) on delete cascade, rating integer not null check (rating between 1 and 5), review text default '', vendor_response text default '', created_at timestamptz not null default now()
);
create table if not exists project_quote_requests (
    id uuid primary key default gen_random_uuid(), request_id text not null unique,
    payload jsonb not null default '{}'::jsonb, status text not null default 'New',
    created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);

create index if not exists products_vendor_id_idx on products(vendor_id);
create index if not exists enquiries_vendor_id_idx on enquiries(vendor_id);
create index if not exists enquiries_buyer_id_idx on enquiries(buyer_id);
create index if not exists quotations_vendor_id_idx on quotations(vendor_id);
create index if not exists orders_vendor_id_idx on orders(vendor_id);
create index if not exists users_role_idx on users(role);
create index if not exists project_quote_requests_customer_idx on project_quote_requests ((payload->>'customer_id'));
create index if not exists project_quote_requests_builder_idx on project_quote_requests ((payload->>'builder_id'));

-- The Streamlit server uses the key in Streamlit secrets. Enable RLS and add
-- policies appropriate to the chosen key/JWT strategy before production use.
