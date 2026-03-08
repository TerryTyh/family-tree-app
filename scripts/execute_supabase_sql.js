const axios = require('axios');

// 配置信息
const SUPABASE_URL = 'https://ipnslrdmrbnwkmulwduj.supabase.co';
const SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwbnNscmRtcmJud2ttdWx3ZHVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjM2OTMyNiwiZXhwIjoyMDg3OTQ1MzI2fQ.RJdNGIhHFy8HjFfKM_fKI99xY983st3JyMkl7EksQpk';

// SQL语句
const SQL = `
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
`;

// 执行SQL的核心函数
async function executeSupabaseSQL() {
  try {
    const response = await axios.post(
      `${SUPABASE_URL}/rest/v1/rpc/exec_sql`, // 专门执行SQL的RPC端点
      { sql: SQL },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`, // 鉴权头
          'apikey': SUPABASE_SERVICE_KEY // 额外的apikey头（Supabase要求）
        },
        // 解决SSL错误的关键配置（如果遇到证书问题）
        httpsAgent: new (require('https').Agent)({
          rejectUnauthorized: false // 临时关闭SSL验证（仅测试用，生产环境不建议）
        })
      }
    );

    console.log('SQL执行成功！', response.data);
  } catch (error) {
    console.error('SQL执行失败：', error.response?.data || error.message);
  }
}

// 运行函数
executeSupabaseSQL();
