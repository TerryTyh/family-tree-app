-- 创建members表
CREATE TABLE IF NOT EXISTS members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(10),
    birth_date DATE,
    birth_time TIME,
    ba_zi TEXT,
    lunar_birth_date TEXT,
    death_date DATE,
    photo TEXT,
    bio TEXT,
    father_id UUID REFERENCES members(id),
    mother_id UUID REFERENCES members(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 创建spouses表
CREATE TABLE IF NOT EXISTS spouses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_id UUID NOT NULL REFERENCES members(id),
    spouse_id UUID NOT NULL REFERENCES members(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(member_id, spouse_id)
);

-- 创建children表
CREATE TABLE IF NOT EXISTS children (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID NOT NULL REFERENCES members(id),
    child_id UUID NOT NULL REFERENCES members(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(parent_id, child_id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_members_name ON members(name);
CREATE INDEX IF NOT EXISTS idx_spouses_member_id ON spouses(member_id);
CREATE INDEX IF NOT EXISTS idx_spouses_spouse_id ON spouses(spouse_id);
CREATE INDEX IF NOT EXISTS idx_children_parent_id ON children(parent_id);
CREATE INDEX IF NOT EXISTS idx_children_child_id ON children(child_id);
