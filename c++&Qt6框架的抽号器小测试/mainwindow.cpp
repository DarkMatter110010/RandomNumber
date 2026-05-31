#include "mainwindow.h"
#include <QStatusBar>

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent)
{
    initUI();
    createMenu();
    loadJsonData();
}

MainWindow::~MainWindow() {}

void MainWindow::initUI() {
    this->setWindowTitle("抽号器");
    this->resize(600, 400);
    this->setWindowFlags(this->windowFlags() | Qt::WindowStaysOnTopHint);

    QWidget* centerWidget = new QWidget(this);
    QVBoxLayout* layout = new QVBoxLayout(centerWidget);

    m_resultLabel = new QLabel("", this);
    m_resultLabel->setAlignment(Qt::AlignCenter);
    m_resultLabel->setStyleSheet("QLabel { font-size: 200px; font-weight: bold; color: #333; border: 2px solid #ccc; border-radius: 10px; background-color: #f9f9f9; }");
    layout->addWidget(m_resultLabel);

    QWidget* btnContainer = new QWidget(this);
    QHBoxLayout* btnLayout = new QHBoxLayout(btnContainer);

    m_drawBtn = new QPushButton("开始抽号", this);
    m_drawBtn->setStyleSheet("QPushButton { font-size: 20px; padding: 10px; background-color: #0078d7; color: white; border-radius: 5px; }");
    btnLayout->addWidget(m_drawBtn);

    m_clearBtn = new QPushButton("清空", this);
    m_clearBtn->setStyleSheet("QPushButton { font-size: 20px; padding: 10px; background-color: #e0e0e0; color: black; border-radius: 5px; }");
    btnLayout->addWidget(m_clearBtn);

    layout->addWidget(btnContainer);
    this->setCentralWidget(centerWidget);

    connect(m_drawBtn, &QPushButton::clicked, this, [this]() {
        int result = getWeightedRandom();
        if (result != -1) {
            m_resultLabel->setText(QString::number(result));
        }
        else {
            QMessageBox::warning(this, "错误", "数据为空！");
        }
        });

    connect(m_clearBtn, &QPushButton::clicked, this, [this]() {
        m_resultLabel->setText("");
        });
}

void MainWindow::createMenu() {
    QMenuBar* menuBar = this->menuBar();
    QMenu* fileMenu = menuBar->addMenu("文件");

    // 1. 修改范围
    QAction* actionRange = new QAction("修改范围", this);
    fileMenu->addAction(actionRange);
    connect(actionRange, &QAction::triggered, this, [this]() {
        RangeDialog dialog(this);
        if (dialog.exec() == QDialog::Accepted) {
            int start = dialog.getStart();
            int end = dialog.getEnd();

            // --- 只有在这里，我们才重置数据 ---
            m_numbers.clear();
            for (int i = start; i <= end; ++i) {
                m_numbers[i] = 1; // 新范围默认权重为1
            }
            saveJsonData(); // 只有修改范围时，才写入文件
            QMessageBox::information(this, "成功", "范围已重置，权重已恢复默认");
        }
        });

    // 2. 修改权重
    QAction* actionWeight = new QAction("修改权重", this);
    fileMenu->addAction(actionWeight);
    connect(actionWeight, &QAction::triggered, this, [this]() {
        if (m_numbers.isEmpty()) {
            QMessageBox::warning(this, "提示", "请先设置号码范围！");
            return;
        }

        WeightDialog dialog(m_numbers, this);
        dialog.initCurrentWeight();

        // 连接“应用”按钮：只更新内存和文件，不关闭窗口
        connect(dialog.m_btnApply, &QPushButton::clicked, this, [this, &dialog]() {
            int num = dialog.getSelectedNumber();
            int weight = dialog.getSelectedWeight();
            m_numbers[num] = weight; // 更新内存
            saveJsonData();          // 立即保存到文件（持久化权重）
            statusBar()->showMessage(QString("号码 %1 权重已更新为 %2").arg(num).arg(weight), 2000);
            });

        // 连接“确定”按钮：保存并关闭
        connect(dialog.m_btnOK, &QPushButton::clicked, this, [this, &dialog]() {
            int num = dialog.getSelectedNumber();
            int weight = dialog.getSelectedWeight();
            m_numbers[num] = weight;
            saveJsonData();
            dialog.accept();
            });

        // 连接“取消”按钮：不保存
        connect(dialog.m_btnCancel, &QPushButton::clicked, this, [&dialog]() {
            dialog.reject();
            });

        dialog.exec();
        });
}

void MainWindow::loadJsonData() {
    QFile file(m_jsonFile);

    // 1. 尝试读取文件
    if (file.exists()) {
        if (file.open(QIODevice::ReadOnly)) {
            QByteArray data = file.readAll();
            QJsonDocument doc = QJsonDocument::fromJson(data);

            // 2. 检查 JSON 格式是否合法 (isObject 检查)
            if (doc.isObject()) {
                QJsonObject obj = doc.object();
                m_numbers.clear();

                // 3. 尝试解析数据
                bool parseSuccess = true;
                for (auto it = obj.begin(); it != obj.end(); ++it) {
                    // 简单的类型检查，防止 JSON 结构错乱导致崩溃
                    if (it.value().isDouble()) {
                        m_numbers[it.key().toInt()] = it.value().toInt();
                    }
                    else {
                        parseSuccess = false;
                        break;
                    }
                }

                if (parseSuccess) {
                    file.close();
                    return; // 成功加载，直接返回，不做任何修改
                }
            }

            // --- 如果代码运行到这里，说明 JSON 格式错误或解析失败 ---
            file.close();
            QMessageBox::critical(this, "错误", "检测到 number.json 文件损坏或格式错误！\n系统将自动重置为默认数据。");
        }
    }

    // --- 4. 执行重置逻辑 (无论是文件不存在，还是上面报错了，都会走到这里) ---
    // 清空内存数据
    m_numbers.clear();

    // 重新生成默认数据 (1-50, 权重 1)
    for (int i = 1; i <= 50; ++i) {
        m_numbers[i] = 1;
    }

    // 强制写入文件，修复损坏的 JSON
    saveJsonData();
}

void MainWindow::saveJsonData() {
    QJsonObject obj;
    for (auto it = m_numbers.begin(); it != m_numbers.end(); ++it) {
        obj[QString::number(it.key())] = it.value();
    }
    QFile file(m_jsonFile);
    if (file.open(QIODevice::WriteOnly)) {
        file.write(QJsonDocument(obj).toJson());
        file.close();
    }
}

int MainWindow::getWeightedRandom() {
    if (m_numbers.isEmpty()) return -1;
    int totalWeight = 0;
    for (auto weight : m_numbers) totalWeight += weight;
    if (totalWeight == 0) return -1;

    int randomValue = QRandomGenerator::global()->bounded(totalWeight);
    int current = 0;
    for (auto it = m_numbers.begin(); it != m_numbers.end(); ++it) {
        current += it.value();
        if (randomValue < current) return it.key();
    }
    return m_numbers.begin().key();
}